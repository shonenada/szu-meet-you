#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16

@author: Lyd
'''
from sqlalchemy import Table, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import mapper, Session

from szumu.database import metadata


session = Session()


class BaseBuilding():

    def __init__(self, title):
        self.title = title


building_table = Table('buildings', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('title', String(250)),
                       Column('ownerid', Integer),
                       Column('mapid', Integer),
                       Column('mapside', Integer),
                       Column('pic', String(250), default='nopic.jpg'),
                       Column('color', String(30), default='brown'),
                       Column('descr', String),
                       Column('special', String),
                       Column('created', DateTime)
                       )


mapper(BaseBuilding, building_table)
