# coding: utf-8
from tornado import gen
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from tornado_router.web import TrfRequestHandler, route, TrfApplication


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


if __name__ == '__main__':
    app = TrfApplication([(r"/api", TrfHandler)])
    server = HTTPServer(app)
    print 8988
    server.listen(8988)
    IOLoop.current().start()
