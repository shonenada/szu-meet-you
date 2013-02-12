#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from szumu.base import Application
from szumu.database import dbmaster
from szumu.modules import modules


def app_root():
    app_root = os.path.dirname(os.path.realpath(__file__)) + "/"
    return app_root


def create_app(config_file):
    app = Application(modules)

    app.load_route()

    app.load_config_from_file(config_file)
    app.load_config_from_file(app_root() + "settings.py")

    dbmaster.init_app(app)

    app.deploy()

    return app
