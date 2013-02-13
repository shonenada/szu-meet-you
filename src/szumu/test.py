#-*- coding: utf-8 -*-
from szumu.web import Controller
from szumu.base import route
from szumu.user import services

@route('/test')
class Test(Controller):
    def get(self):
        userid = services.get_id_by_username(u"shonenada@gmail.com")
        self.write(unicode(userid))