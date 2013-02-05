#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

import szumu.web
from szumu.users import model
from szumu.base import route


@route(r"/office")
class Office(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404, 'Not Found')
    
    @tornado.web.authenticated
    def post(self):
        message = []
        user = self.get_current_user()
        
        truename = unicode(self.get_argument('truename', None)).strip()
        birthday = unicode(self.get_argument('birthday', '0000-00-00')).strip()
        number = unicode(self.get_argument('number', None)).strip()
        college = unicode(self.get_argument('college', 0)).strip()
        phone = unicode(self.get_argument('phone', 0)).strip()
        short = unicode(self.get_argument('short', 0)).strip()
        qq = unicode(self.get_argument('qq', 0)).strip()
        
        success = True
        
        if not truename:
            message.append('真实姓名不能为空')
            success = False
    
        if model.User.check_truename(self.db, truename, user.username):
            success = False
            message.append('姓名已存在，若您未曾登记过信息，请联系站长')
            
        if model.User.check_number(self.db, number, user.username):
            success = False
            message.append('学号已存在，若您未曾登记过信息，请联系站长')
            
        if birthday == '0000-00-00':
            message.append('生日不能为空')
            success = False
            
        if not number:
            message.append('学号不能为空')
            success = False
            
        if college == 0:
            message.append('学院不能为空')
            success = False
            
        if success:
            user.truename = truename
            user.birthday = birthday
            user.number = number
            user.college = college
            user.phone = phone
            user.shortPhone = short
            user.qq = qq
            user.state = 3            
            user.reg_the_identity()
        
        self.finish({'success':success,'message':message})

