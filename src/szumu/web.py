#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
from datetime import date, datetime

import tornado
import tornado.web

from szumu.user.services import find


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

    @property
    def current_user(self):
        user_id = self.get_secure_cookie('userinfor')
        if not user_id:
            return None
        current_user = find(user_id)
        return current_user

    def check_whether_logged(self):
        user = self.current_user
        if not user is None:
            self.redirect('/')

    def check_whether_finish_truename_and_number(self):
        user = self.current_user
        if not user:
            raise tornado.web.HTTPError(403)
        truename = user.truename
        number = user.number
        if not truename:
            raise tornado.web.HTTPError(403, 'Please input your truename')
        if not number:
            raise tornado.web.HTTPError(403, 'Please input your number')
