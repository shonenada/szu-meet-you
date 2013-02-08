#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.database


class DbMaster():

    db = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        self.db = tornado.database.Connection(host=self.app.config['db_host'],
                                     database=self.app.config['db_name'],
                                     user=self.app.config['db_user'],
                                     password=self.app.config['db_pass'])
        DbMaster.db = self.db


db = DbMaster.db
