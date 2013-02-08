#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
from datetime import date, datetime

import tornado

from szumu.database import DbMaster
from szumu.users import model

httperror = tornado.web.HTTPError
asynchronous = tornado.web.asynchronous
auth = tornado.web.authenticated


''' make json able to encode datetime ''' 
def __default(obj):
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
        if not user_id or user_id == None: return None
        user = DbMaster.db.get("SELECT * FROM szu_mu_user WHERE id = %s ", int(user_id) )
        return model.User(user['username'], user['password'], user['nickname'], user['gender'], self.request.remote_ip)

    def check_whether_logged(self):
        user = self.get_current_user()
        if not user == None:
            self.redirect('/home')

    def check_whether_finish_truename_and_number(self):
        user = self.get_current_user()
        if not user: raise httperror(403)
        user = user.as_array()
        truename = user['truename']
        number = user['number']
        if not truename: raise httperror(403, 'Please input your truename')
        if not number: raise httperror(403, 'Please input your number')
