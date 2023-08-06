# coding: utf-8
import re
from tornado import escape
from tornado import httputil
from tornado import iostream
from tornado.concurrent import is_future
from tornado.gen import Future
from tornado.httputil import HTTPServerRequest
from tornado.log import app_log
from tornado.web import RequestHandler, StaticFileHandler, RedirectHandler, ErrorHandler, HTTPError
from tornado.web import Application
from tornado import gen


def unquote_or_none(s):
    """None-safe wrapper around url_unescape to handle unamteched optional
    groups correctly.

    Note that args are passed as bytes so the handler can decide what
    encoding to use.
    """
    if s is None:
        return s
    return escape.url_unescape(s, encoding=None, plus=False)


def has_stream_request_body(cls):
    if not issubclass(cls, RequestHandler):
        raise TypeError("expected subclass of RequestHandler, got %r", cls)
    return getattr(cls, '_stream_request_body', False)


def route(endpoint=None, allow_method=None):
    def wrapper(api_method):
        setattr(api_method, "_custom", True)
        setattr(api_method, "_endpoint", endpoint)
        setattr(api_method, "_allow_method", allow_method or ["get"])
        return api_method

    return wrapper


class RequestHandlerMeta(type):
    def __new__(mcs, name, base, attrs):
        endpoint_map = {}
        for k, v in attrs.iteritems():
            if callable(v) and hasattr(v, "_custom"):
                endpoint = getattr(v, "_endpoint") or "/{}".format(k)
                allow_method = getattr(v, "_allow_method") or ["get"]
                for verb in allow_method:
                    assert verb.upper() in RequestHandler.SUPPORTED_METHODS, ("verb: {} is not supported".format(verb))
                endpoint_map[endpoint] = (k, allow_method)

        attrs["_END_POINT_MAP"] = endpoint_map
        return type.__new__(mcs, name, base, attrs)


class TrfHTTPServerRequest(HTTPServerRequest):
    @property
    def endpoint(self):
        return self._endpoint if hasattr(self, "_endpoint") else "/"

    @endpoint.setter
    def endpoint(self, v):
        setattr(self, "_endpoint", v)


class TrfRequestHandler(RequestHandler):
    __metaclass__ = RequestHandlerMeta

    def __init__(self, application, request, **kwargs):
        """

        :param application:
        :param request:
        :param kwargs:
        """
        RequestHandler.__init__(self, application, request, **kwargs)
        # endpoint_map: {"/test": (func_name, [get, post])}
        self.endpoint_map = self._END_POINT_MAP if hasattr(self, "_END_POINT_MAP") else dict()

    @gen.coroutine
    def _execute(self, transforms, *args, **kwargs):
        """
        重新定制请求映射方法
        :param transforms:
        :param args:
        :param kwargs:
        :return:
        """
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            self.path_args = [self.decode_argument(arg) for arg in args]
            self.path_kwargs = {k: self.decode_argument(v, name=k) for (k, v) in kwargs.items()}

            # If XSRF cookies are turned on, reject form submissions without
            # the proper cookie
            if self.request.method not in ("GET", "HEAD", "OPTIONS") and \
                    self.application.settings.get("xsrf_cookies"):
                self.check_xsrf_cookie()

            result = self.prepare()
            if is_future(result):
                result = yield result
            if result is not None:
                raise TypeError("Expected None, got %r" % result)
            if self._prepared_future is not None:
                # Tell the Application we've finished with prepare()
                # and are ready for the body to arrive.
                self._prepared_future.set_result(None)
            if self._finished:
                return

            if has_stream_request_body(self.__class__):
                try:
                    yield self.request.body
                except iostream.StreamClosedError:
                    return

            if self.request.end_point == "/":
                method = getattr(self, self.request.method.lower())
            else:
                handler_func = self.endpoint_map.get(self.request.end_point)
                if not handler_func:
                    raise HTTPError(404)
                func_allow_methods = handler_func[1]
                if self.request.method not in map(lambda x: x.upper(), func_allow_methods):
                    raise HTTPError(405)
                method = getattr(self, handler_func[0])
            result = method(*self.path_args, **self.path_kwargs)
            if is_future(result):
                result = yield result
            if result is not None:
                raise TypeError("Expected None, got %r" % result)
            if self._auto_finish and not self._finished:
                self.finish()
        except Exception as e:
            try:
                self._handle_request_exception(e)
            except Exception:
                app_log.error("Exception in exception handler", exc_info=True)
            if (self._prepared_future is not None and
                    not self._prepared_future.done()):
                # In case we failed before setting _prepared_future, do it
                # now (to unblock the HTTP server).  Note that this is not
                # in a finally block to avoid GC issues prior to Python 3.4.
                self._prepared_future.set_result(None)


class TrfURLSpec(object):
    """
    定制路由映射对象，将路由前缀映射到单个handler，由endpoint一一对应handler方法
    """

    def __init__(self, pattern, handler, kwargs=None, name=None):
        endpoint_map = handler._END_POINT_MAP if hasattr(handler, "_END_POINT_MAP") else dict()
        self.regex_list = []
        for endpoint in endpoint_map:
            compile_pattern = pattern + endpoint + "$"
            regex = re.compile(compile_pattern)
            assert len(regex.groupindex) in (0, regex.groups), \
                ("groups in url regexes must either be all named or all ",
                 "positional: %r" % regex.pattern)
            self.regex_list.append((regex, endpoint))

        default_pattern = pattern + "$"
        default_regex = re.compile(default_pattern)
        self.regex_list.append((default_regex, "/"))
        self.handler_class = handler
        self.kwargs = kwargs or dict()
        self.name = name

    def __repr__(self):
        return ""


class TrfRequestDispatcher(httputil.HTTPMessageDelegate):
    def __init__(self, application, connection):
        self.application = application
        self.connection = connection
        self.request = None
        self.chunks = []
        self.handler_class = None
        self.handler_kwargs = None
        self.path_args = []
        self.path_kwargs = {}

    def headers_received(self, start_line, headers):
        self.set_request(TrfHTTPServerRequest(
            connection=self.connection, start_line=start_line,
            headers=headers))
        if self.stream_request_body:
            self.request.body = Future()
            return self.execute()

    def set_request(self, request):
        self.request = request
        self._find_handler()
        self.stream_request_body = has_stream_request_body(self.handler_class)

    def _find_handler(self):
        """
        重新定制路由映射方法
        :return:
        """
        app = self.application
        handlers = app._get_host_handlers(self.request)
        if not handlers:
            self.handler_class = RedirectHandler
            self.handler_kwargs = dict(url="{}://{}/".format(self.request.protocol, app.default_host))
            return

        for spec in handlers:
            for regex, endpoint in spec.regex_list:
                match = regex.match(self.request.path)
                if match:
                    self.handler_class = spec.handler_class
                    self.handler_kwargs = spec.kwargs
                    self.request.end_point = endpoint
                    if regex.groups:
                        if regex.groupindex:
                            self.path_kwargs = {
                                str(k): unquote_or_none(v) for (k, v) in match.groupdict().items()
                                }
                        else:
                            self.path_args = map(lambda s: unquote_or_none(s), match.groups())

                    return

        if app.settings.get("default_handler_class"):
            self.handler_class = app.settings['default_handler_class']
            self.handler_kwargs = app.settings.get(
                'default_handler_args', {})
        else:
            self.handler_class = ErrorHandler
            self.handler_kwargs = dict(status_code=404)

    def data_received(self, data):
        if self.stream_request_body:
            return self.handler.data_received(data)
        else:
            self.chunks.append(data)

    def finish(self):
        if self.stream_request_body:
            self.request.body.set_result(None)
        else:
            self.request.body = b''.join(self.chunks)
            self.request._parse_body()
            self.execute()

    def on_connection_close(self):
        if self.stream_request_body:
            self.handler.on_connection_close()
        else:
            self.chunks = None

    def execute(self):
        # If template cache is disabled (usually in the debug mode),
        # re-compile templates and reload static files on every
        # request so you don't need to restart to see changes
        if not self.application.settings.get("compiled_template_cache", True):
            with RequestHandler._template_loader_lock:
                for loader in RequestHandler._template_loaders.values():
                    loader.reset()
        if not self.application.settings.get('static_hash_cache', True):
            StaticFileHandler.reset()

        self.handler = self.handler_class(self.application, self.request,
                                          **self.handler_kwargs)
        transforms = [t(self.request) for t in self.application.transforms]

        if self.stream_request_body:
            self.handler._prepared_future = Future()
        # Note that if an exception escapes handler._execute it will be
        # trapped in the Future it returns (which we are ignoring here,
        # leaving it to be logged when the Future is GC'd).
        # However, that shouldn't happen because _execute has a blanket
        # except handler, and we cannot easily access the IOLoop here to
        # call add_future (because of the requirement to remain compatible
        # with WSGI)
        f = self.handler._execute(transforms, *self.path_args,
                                  **self.path_kwargs)
        # If we are streaming the request body, then execute() is finished
        # when the handler has prepared to receive the body.  If not,
        # it doesn't matter when execute() finishes (so we return None)
        return self.handler._prepared_future


class TrfApplication(Application):
    def start_request(self, server_conn, request_conn):
        # Modern HTTPServer interface
        return TrfRequestDispatcher(self, request_conn)

    def add_handlers(self, host_pattern, host_handlers):
        """
        更换路由映射对象
        :param host_pattern:
        :param host_handlers:
        :return:
        """
        if not host_pattern.endswith("$"):
            host_pattern += "$"
        handlers = []
        if self.handlers and self.handlers[-1][0].pattern == '.*$':
            self.handlers.insert(-1, (re.compile(host_pattern), handlers))
        else:
            self.handlers.append((re.compile(host_pattern), handlers))

        for spec in host_handlers:
            if isinstance(spec, (tuple, list)):
                assert len(spec) in (2, 3, 4)
                spec = TrfURLSpec(*spec)
            handlers.append(spec)
            if spec.name:
                if spec.name in self.named_handlers:
                    app_log.warning(
                        "Multiple handlers named %s; replacing previous value",
                        spec.name)
                self.named_handlers[spec.name] = spec
