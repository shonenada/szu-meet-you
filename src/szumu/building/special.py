#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16
@author: Lyd
'''

from szumu.config import buildings
from szumu.building.base import BaseBuilding
from szumu.building.services import find_special


def build_special(building_config):
    special = BaseBuilding(building_config['title'])
    special.ownerid = building_config['ownerid']
    special.pic = building_config['pic']
    special.mapid = building_config['mapid']
    special.mapsite = building_config['mapsite']
    special.color = building_config['color']
    special.descr = building_config['descr']
    special.special = building_config['special']
    return special

office = build_special(buildings.OFFICE)
student_center = build_special(buildings.STUDENT_CENTER)
stone = build_special(buildings.STONE)
tech = build_special(buildings.TECH)
teach = build_special(buildings.TEACH)
litera = build_special(buildings.LITERA)
northlib = build_special(buildings.NORTH)
southlib = build_special(buildings.SOUTH)
gym = build_special(buildings.GYM)
dorm = build_special(buildings.DORM)
being_built = build_special(buildings.BEING_BUILT)
being_rent = build_special(buildings.RENT)
classroom = None
teach.college_no = buildings.TEACH_COLLEGE_NO

    # def createShop(self, id):
    #     shop = DbMaster.db.get("SELECT * FROM szu_mu_building WHERE "
    #                            "id = %s AND special = 'rent'", int(id))
    #     self.id = shop['id']
    #     self.title = shop['title']
    #     self.ownerid = shop['ownerid']
    #     self.pic = shop['pic']
    #     self.color = shop['color']
    #     self.special = shop['special']
    #     self.descr = shop['descr']

    # @staticmethod
    # def find(id):
    #     return find_special(id, 'rent')


special_map = {'office': office,
               'northlib': northlib,
               'southlib': southlib,
               'teach': teach,
               'tech': tech,
               'litera': litera,
               'student': student_center,
               'stone': stone,
               'gym': gym,
               'dorm': dorm,
               'rent': being_rent}
