#/usr/bin/env python

import tornado.web

from szumu.base import route


@route('/')
class Home(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', title="title", descr="descr", msgs={})


@route('/aboutus')
class AboutUs(tornado.web.RequestHandler):
    """ about us handler """
    def get(self):
        self.render('infor/aboutus.html')


@route('/contactus')
class ContactUs(tornado.web.RequestHandler):
    """ contact us handler """
    def get(self):
        self.render('infor/contactus.html')
