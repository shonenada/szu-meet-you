#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-18

@author: Lyd
'''
from web import Controller,httperror
import szumu.chat

from szumu.map.model import Map
from config.buildingConfig import buildingConfig

from szumu.building.BaseBuilding import BaseBuilding
from szumu.building.special import *
from szumu.building.shop.model import Shop

chat =  szumu.chat.handler.msgsrv

class MapHandler(Controller):
    
    def get(self, mapid):
        mapid = unicode(mapid).strip()
        map = Map.find(self.db, int(mapid))
        if not map:
            raise httperror(404, "Not Found")
        
        link = map.link.split(',')
        path = map.path.split(',')
        build = map.buildings.split(',')
        
        buildings = {}
        i = 0

        for x in build:
            if not x or x == 'None':
                buildings[i] = None
            elif x in special_map:
                buildings[i] = special_map[x].tostring()
            else:
                buildings[i] = BaseBuilding.find(self.db, x)
            i = i + 1
        
        current_user = self.get_current_user()
        if not current_user == None:
            current_user = current_user.as_array()

        self.set_cookie('lastview', mapid)

        special = [x['id'] for x in buildingConfig.szumu_building_rent_type]
        special.append('rent')
        
        self.render('map.html', 
                        map=map.link, 
                        title=map.title, descr=map.descr, 
                        link=link,
                        path=path,
                        buildings=buildings,
                        msgs=chat.messages,
                        special=special,
                    )
    
    def post(self):
        raise httperror(403, "Forbidden")
    
    
    
class ViewLastMapHandler(Controller):
    def get(self):
        lastview = unicode(self.get_cookie('lastview'))
        if lastview:
            self.redirect('/map/' + lastview)
        else:
            raise httperror(404, 'Not Found')
    
    def post(self):
        raise httperror(403, 'Forbidden')