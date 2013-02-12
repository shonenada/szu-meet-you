#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import create_engine, MetaData


class DbMaster():

    engine = None
    metadata = None

    def init_app(self, app, connect=True):
        self.app = app
        if connect:
            self.connect()

    def connect(self):
        self.engine = create_engine(self.app.config['db_uri'])
        self.metadata = MetaData(self.engine)
        DbMaster.engine = self.engine
        DbMaster.metadata = self.metadata


dbmaster = DbMaster()
metadata = DbMaster.metadata
