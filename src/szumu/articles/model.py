#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-10-2

@author: Lyd
'''

from szumu.database import dbMaster  

class Aritcles(dbMaster):
    ''' 文章模型  '''
    
    id = None
    title = None
    content = None
    author = None
    shopid = None
    special = None
    created = None
    
    def __init__(self, title):
        dbMaster.__init__(self)
        self.title = title
        dbMaster.connect(self)
        
    def save(self):
        if not self.db:
            return None
        if not self.title:
            return None
        if not self.content:
            return None
        if not self.author:
            return None
         
        return self.db.execute("INSERT INTO `szu_mu_articles` (title, content, author, shopid, special) "
                               "VALUE (%s, %s, %s, %s, %s)",
                                self.title, self.content,
                                self.author, self.shopid, self.special )

    def remove(self):        
        if not self.db:
            return None
        if not self.id:
            return None

        return self.db.execute("DELETE FROM `szu_mu_articles` WHERE id = %s", int(self.id))
        
        
        
    @staticmethod
    def find(db, id):
        if not db:
            return None
        if not id:
            return None
        return db.get("SELECT * FROM `szu_mu_articles` WHERE id = %s ", int(id))
    
    @staticmethod
    def findByAuthor(db, authorid):
        if not db:
            return None
        if not authorid:
            return None
        return db.query("SELECT * FROM `szu_mu_articles` WHERE author = %s ORDER BY id DESC", int(authorid))
    
    @staticmethod
    def findByShopid(db, shopid):
        if not db:
            return None
        if not shopid:
            return None
        return db.query("SELECT * FROM `szu_mu_articles` WHERE shopid = %s ORDER BY id DESC", int(shopid))
        
        
        
        
        
        
        