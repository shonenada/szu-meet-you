#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
from datetime import date, datetime

import tornado

from szumu.user.services import find


httperror = tornado.web.HTTPError
asynchronous = tornado.web.asynchronous
auth = tornado.web.authenticated


def __default(obj):
    '''make json able to encode datetime'''
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)


def json_encode(o):
    return json.dumps(o, default=__default)


class Controller(tornado.web.RequestHandler):

    def get_current_user(self, user_id=None):
        if not user_id:
            user_id = self.get_secure_cookie('userinfor')
        if not user_id or user_id is None:
            return None
        user = find(user_id)
        return user
