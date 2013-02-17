#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os.path

import tornado.web


class Application(tornado.web.Application):

    def __init__(self, modules=[], config={}):
        self.handlers = []
        self.modules = modules
        self.config = config

    def init_modules(self, modules=[]):
        self.modules = modules

    def load_route(self):
        for module in self.modules:
            handler = (module.url, module)
            self.handlers.append(handler)

    def deploy(self):
        tornado.web.Application.__init__(self, self.handlers, **self.config)

    def load_config_from_file(self, file):
        conf_file = open(file, "r")
        conf = conf_file.readlines()
        for line in conf:
            config_line = line.strip().split('=')
            conf_name = config_line[0].lower()
            conf_var = config_line[1]
            cmd = "new_conf = dict(" + conf_name + '=' + conf_var + ")"
            exec(cmd)
            self.config = dict(self.config, **new_conf)


def route(url):
    def handler(cls):
        cls.url = url
        return cls
    return handler
