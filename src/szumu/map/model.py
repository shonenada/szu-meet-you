#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Map(object):
    """ The model of Map information """
    
    mid = None
    title = None
    descr = None
    path = [0,0,0,0]        # up right down left
    link = [None,None,None,None]            #up right down left
    buildings = {
                 0:None,
                 1:None,
                 2:None,
                 3:None,
                 4:None,
                 5:None,
                 6:None,
                 7:None,
                 8:None,
                 9:None,
                 10:None,
                 11:None,
                 12:None,
                 13:None,
                 14:None,
                 }
    created = None
    
    def __init__(self, title, descr=None, path=[], link=[], buildings={}):
        self.title = title
        self.descr = descr
        self.path = path
        self.link = link
        self.buildings = buildings
        
        
    @staticmethod
    def find(db, id):
        db = db.get("SELECT * FROM szu_mu_map WHERE id = %s", id)
        if not db :
            return None
        map = Map(db['title'], db['descr'], db['path'], db['link'], db['buildings'])
        map.mid = id
        return map
    






