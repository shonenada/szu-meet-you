#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16

@author: Lyd
'''

from szumu.dbMaster.dbMaster import dbMaster

class BaseBuilding(dbMaster):
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
        dbMaster.__init__(self)
        self.title = title
        dbMaster.connect(self)
        
    @staticmethod
    def find(db, id):
        if not id or id == 'None':
            return None
        else:
            return db.get("SELECT * FROM szu_mu_building WHERE `id` = %s", int(id))
        
        