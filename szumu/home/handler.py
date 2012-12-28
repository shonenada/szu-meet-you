#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

class HomeHandler(tornado.web.RequestHandler):
    """ Build the handler of home """
    def get(self):
        """ Rewrite GET method. """
        self.render('index.html')
    
    def post(self, username, password):
        """ Check for the username and password. """
        pass