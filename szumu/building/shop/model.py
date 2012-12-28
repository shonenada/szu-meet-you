#!/usr/bin/evn python
#-*- coding: utf-8 -*-

from szumu.building.BaseBuilding import BaseBuilding
from szumu.articles.model import Aritcles

class Shop(BaseBuilding):
    
    """
        Table name : shops
        Columns:
            1# id
            2# title
            3# ownerid
            4# pic
            5# mapid
            6# mapsite
            7# descr
            8# sepical = Shop
    """
    
    def __init__(self, title, ownerid):
        BaseBuilding.__init__(self,title)
        self.ownerid = ownerid
    
    def update(self):
        if not self.db:
            return None
        shop = self.db.get("SELECT * FROM `szu_mu_building` WHERE id = %s", int(self.id))
        if not shop:
            return None
        if not shop['ownerid'] == self.ownerid:
            return None
        return self.db.execute("UPDATE `szu_mu_building` SET title = %s, descr = %s WHERE id = %s ",self.title, self.descr, int(self.id))
    
    @staticmethod
    def getCurrentUserShop(db, userid):
        return db.get("SELECT * FROM `szu_mu_building` WHERE `ownerid` = %s", userid)

    
class PrivateShop(Shop):
    
    @staticmethod
    def getArticlesByShopid(db, shopid):
        if not db or not shopid:
            return None
        return Aritcles.findByShopid(db, shopid)
    
    @staticmethod
    def find(db, id):
        if not db or not id:
            return None
        return db.get("SELECT * FROM `szu_mu_building` WHERE id = %s AND special = 'shop/private' ", int(id))

class SellShop(Shop):
    
    @staticmethod
    def find(db, id):
        if not db or not id:
            return None
        return db.get("SELECT * FROM `szu_mu_building` WHERE id = %s AND special = 'shop/sell' ", int(id))