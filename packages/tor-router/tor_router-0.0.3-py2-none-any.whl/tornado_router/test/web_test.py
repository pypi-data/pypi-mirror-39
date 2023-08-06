# coding: utf-8

import unittest

from tornado import gen
from tornado.testing import AsyncHTTPTestCase

from tornado_router.web import RequestHandlerMeta, route, TrfRequestHandler, TrfApplication


class RequestHandlerMetaTest(unittest.TestCase):
    def test_handler(self):

        class A(object):
            __metaclass__ = RequestHandlerMeta

            def a(self):
                pass

            def b(self):
                pass

            def c(self):
                pass

            c._is_custom = True

        self.assertIn("_END_POINT_MAP", A.__dict__)
        self.assertDictEqual(getattr(A, "_END_POINT_MAP"), {})

    def test_route(self):
        class B(object):
            __metaclass__ = RequestHandlerMeta

            def a(self):
                return

            @route("/a", allow_method=["get"])
            def b(self):
                return "b"

            @route("/c")
            def c(self):
                pass

            @route(allow_method=["get"])
            def d(self):
                pass

            @route()
            def e(self):
                pass

            @route(allow_method=["GET"])
            def f(self):
                pass

        ins = B()
        self.assertIn("/a", getattr(B, "_END_POINT_MAP"))
        self.assertIn("/c", getattr(B, "_END_POINT_MAP"))
        self.assertIn("/d", getattr(B, "_END_POINT_MAP"))
        self.assertIn("/e", getattr(B, "_END_POINT_MAP"))
        self.assertEqual("b", ins.b())

        try:

            class C(object):
                __metaclass__ = RequestHandlerMeta

                @route(allow_method=["get", "gets", "post"])
                def c(self):
                    pass
        except Exception as e:
            self.assertIsInstance(e, AssertionError)


class TrfHandler(TrfRequestHandler):
    def get(self, *args, **kwargs):
        self.write("get ok")
        self.finish()

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.write("post ok")
        self.finish()

    @route("/hello")
    def say_hello(self, *args, **kwargs):
        self.write("hello")
        self.finish()

    @route("/hi")
    @gen.coroutine
    def say_hi(self, *args, **kwargs):
        self.write("hi")
        self.finish()

    @route("/fine", allow_method=["get", "post", "put"])
    @gen.coroutine
    def say_fine(self, *args, **kwargs):
        self.write("fine")
        self.finish()


class TrfApplicationTest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = TrfApplication(self.get_handlers(), **self.get_app_kwargs())
        return self.app

    def get_handlers(self):
        return [(r"/api", TrfHandler)]

    def get_app_kwargs(self):
        return {}

    def test_get(self):
        response = self.fetch("/api")
        self.assertEqual(response.body, "get ok")

    def test_post(self):
        response = self.fetch("/api", method="POST", body="")
        self.assertEqual(response.body, "post ok")

    def test_hello(self):
        response = self.fetch("/api/hello")
        self.assertEqual(response.body, "hello")
        response = self.fetch("/api/hello", method="POST", body="")
        self.assertEqual(response.code, 405)

    def test_hi(self):
        response = self.fetch("/api/hi")
        self.assertEqual(response.body, "hi")
        response = self.fetch("/api/hi", method="POST", body="")
        self.assertEqual(response.code, 405)

    def test_fine(self):
        response = self.fetch("/api/fine")
        self.assertEqual(response.body, "fine")
        response = self.fetch("/api/fine", method="POST", body="")
        self.assertEqual(response.body, "fine")
        response = self.fetch("/api/fine", method="PUT", body="")
        self.assertEqual(response.body, "fine")
        response = self.fetch("/api/fine", method="DELETE")
        self.assertEqual(response.code, 405)


if __name__ == '__main__':
    unittest.main()
