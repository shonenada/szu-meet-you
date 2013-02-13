#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-10-2
@author: Lyd
'''
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import mapper, Session

from szumu.database import DbMaster


metadata = DbMaster.metadata
session = Session()


class Aritcle(object):
    ''' 文章模型  '''

    def __init__(self, title):
        self.title = title


article_table = Table('articles', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('title', String(250)),
                      Column('content', Text),
                      Column('author', Integer),
                      Column('shopid', Integer),
                      Column('special', String(50)),
                      Column('created', DateTime, default=datetime.now)
                      )

mapper(Aritcle, article_table)
