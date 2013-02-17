#/usr/bin/env python
#-*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import mapper, Session

from szumu.database import DbMaster


session = Session()
metadata = DbMaster.metadata


class Map(object):

    def __init__(self, title, descr=None):
        self.title = title
        self.descr = descr


map_table = Table('map', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('title', String(250)),
                  Column('descr', Text),
                  Column('path', String(8)),
                  Column('link', String(47)),
                  Column('buildings', Text),
                  Column('created', DateTime, default=datetime.now)
                  )


mapper(Map, map_table)
