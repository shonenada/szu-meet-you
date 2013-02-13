#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime

import tornado
from sqlalchemy import Table, Column, Integer, DateTime
from sqlalchemy.orm import mapper, Session

from szumu.database import DbMaster


session = Session()
metadata = DbMaster.metadata


class RelationShip(object):

    FOCUS = 1
    IGNORE = 0

    def __init__(self, fromid, toid, relationship):
        self.fromid = fromid
        self.toid = toid
        self.relationship = relationship

    def __repr__(self):
        return ("<FromID %r, ToID %r>" % self.fromid, self.toid)


relationship_table = Table('relationship', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('fromid', Integer),
                           Column('toid', Integer),
                           Column('relationship', Integer),
                           Column('created', DateTime, default=datetime.now)
                           )


mapper(RelationShip, relationship_table)
