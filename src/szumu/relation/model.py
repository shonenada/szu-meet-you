#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime

import tornado
from sqlalchemy import Table, Column, Integer, DateTime
from sqlalchemy.orm import mapper, Session

from szumu.database import DbMaster


session = Session()
metadata = DbMaster.metadata


class Relation(object):

    FOCUS = 1
    IGNORE = 0

    def __init__(self, fromid, toid, relation):
        self.fromid = fromid
        self.toid = toid
        self.relation = relation

    def __repr__(self):
        return ("<FromID %r, ToID %r>" % self.fromid, self.toid)


relation_table = Table('relation', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('fromid', Integer),
                       Column('toid', Integer),
                       Column('relation', Integer),
                       Column('created', DateTime, default=datetime.now)
                       )


mapper(Relation, relation_table)
