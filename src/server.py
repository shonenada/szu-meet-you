#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado

from szumu.app import create_app


def run_app():
    app = create_app("production.conf")
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    run_app()
