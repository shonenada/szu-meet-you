#/usr/bin/env python
#-*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, DateTime, Float
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
                  Column('descr', String),
                  Column('path', String(8)),
                  Column('link', String(47)),
                  Column('buildings', String),
                  Column('created', DateTime)
                  )


mapper(Map, map_table)
