#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from szumu.base import Application
from szumu.database import DbMaster, dbmaster


def app_root():
    app_root = os.path.dirname(os.path.realpath(__file__)) + "/"
    return app_root


def create_app(config_file):
    app = Application()

    app.load_config_from_file(config_file)
    app.load_config_from_file(app_root() + "settings.py")

    dbmaster.init_app(app)

    from szumu.modules import modules
    app.init_modules(modules)
    app.load_route()

    app.deploy()

    return app
