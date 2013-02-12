#!/usr/bin/env python
#-*- coding: utf-8 -*-

from hashlib import md5
from datetime import datetime

import tornado
from sqlalchemy import Table, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import mapper, Session

from szumu.database import metadata


session = Session()


class User(object):

    SALT = "WAIT_TO_MODIFY"

    def __init__(self, username, password, nickname):
        self.username = username
        self.hash_password(password)
        self.nickname = nickname

    def __repr__(self):
        return ("<User %r>" % self.username)

    @staticmethod
    def hash_string(salt, raw_string):
        """Hashed a string"""
        hashed_string = md5("<%s|%s>" % (salt, raw_string))
        return hashed_string.hexdigest()

    def hash_password(self, raw_password):
        """hash_password"""
        self.hashed_password = self._hash_password(self.SALT, raw_password)

    def update_log_time(self, log_time=datetime.utcnow()):
        """Update last log time"""
        global session
        self.last_log_time = log_time
        session.commit()

    def update_log_ip(self, log_ip):
        """Update last log ip"""
        global session
        self.last_log_ip = log_ip
        session.commit()

    def update_token(self, token):
        """Update token"""
        global session
        self.token = token
        session.commit()

    @staticmethod
    def _make_token(salt, ip, auth_time):
        return md5("<%s,%s|%s>" % (salt, ip, auth_time)).hexdigest()


user_table = Table('users', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('username', String(70)),
                   Column('hashed_password', String(32)),
                   Column('token', String(32)),
                   Column('nickname', String(20)),
                   Column('number', String(15)),
                   Column('truename', String(10)),
                   Column('gender', Integer),
                   Column('college', Integer),
                   Column('birthday', DateTime),
                   Column('qq', String(15)),
                   Column('created', DateTime, default=datetime.now),
                   Column('reg_ip', String),
                   Column('last_log_time', DateTime),
                   Column('last_log_ip', String),
                   Column('state', Integer, default=1),
                   Column('trash', Integer, default=0),
                   )

mapper(User, user_table)
