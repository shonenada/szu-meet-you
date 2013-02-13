#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime

import tornado
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import mapper, Session

from szumu.database import DbMaster


session = Session()
metadata = DbMaster.metadata


class Message(object):

    READED = 1
    NOT_READED = 0
    
    def __init__(self, fromid, toid, msg, state=NOT_READED):
        self.fromid = fromid
        self.toid = toid
        self.msg = msg
        self.state = state

    def hide_by_from(self):
        """Delete by sender"""
        global session
        self.from_hide = 1
        session.commit()

    def hide_by_to(self):
        """Delete by receiver"""
        global session
        self.to_hide = 1
        session.commit()


message_table = Table('msg', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('fromid', Integer),
                      Column('toid', Integer),
                      Column('msg', String(250)),
                      Column('created', DateTime, default=datetime.now),
                      Column('state', Integer),
                      Column('from_hide', Integer, default=0),
                      Column('to_hide', Integer, default=0)
                      )


mapper(Message, message_table)
