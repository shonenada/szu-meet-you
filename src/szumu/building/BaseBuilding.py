#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16

@author: Lyd
'''

from szumu.database import DbMaster


db = DbMaster.db


class BaseBuilding():
    ''' 基础建筑物 '''
    """
        Columns:
            1# id
            2# title
            3# ownerid
            4# pic
            5# mapid
            6# mapsite
            7# descr
            8# sepcial
            9# created
    """
    
    id = None
    title = None
    ownerid = None
    pic = None
    mapid = None
    mapsite = None
    descr = None
    special = None
    created = None
    
    def __init__(self, title):
        self.title = title
        
    @staticmethod
    def find(id):
        if not id or id == 'None':
            return None
        else:
            return DbMaster.db.get("SELECT * FROM szu_mu_building WHERE `id` = %s", int(id))
        
        