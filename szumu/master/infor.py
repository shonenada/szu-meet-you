#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16

@author: Lyd
'''

from web import Controller

class AboutHandler(Controller):
    """ about us handler """
    def get(self):
        self.render('infor/aboutus.html')
        
    
class ContactHandler(Controller):
    """ contact us handler """
    def get(self):
        self.render('infor/contactus.html')