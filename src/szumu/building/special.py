#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16
@author: Lyd
'''

from szumu.config import buildings
from szumu.building.base import BaseBuilding
from szumu.building.services import find_special


class SpecialBuilding(BaseBuilding):

    def get_infor(self, bd):
        self.title = bd['title']
        self.ownerid = bd['ownerid']
        self.pic = bd['pic']
        self.mapid = bd['mapid']
        self.mapsite = bd['mapsite']
        self.color = bd['color']
        self.descr = bd['descr']
        self.special = bd['special']

    def tostring(self):
        return {'title': self.title,
                'ownerid': self.ownerid,
                'pic': self.pic,
                'mapid': self.mapid,
                'mapsite': self.mapsite,
                'color': self.color,
                'descr': self.descr,
                'special': self.special,
                }


class Office(SpecialBuilding):
    ''' 办公楼 '''
    def __init__(self):
        self.get_infor(buildings.OFFICE)

    def get_announce(self):
        pass


class StudentCenter(SpecialBuilding):
    ''' 学生活动中心 '''
    def __init__(self):
        self.get_infor(buildings.STUDENT_CENTER)


class Stone(SpecialBuilding):
    ''' 石头邬 '''
    def __init__(self):
        self.get_infor(buildings.STONE)


class TechBuilding(SpecialBuilding):
    ''' 科技楼 '''
    def __init__(self):
        self.get_infor(buildings.TECH)


class TeachingBuilding(SpecialBuilding):
    ''' 教学楼  '''

    college_no = buildings.TEACH_COLLEGE_NO

    def __init__(self):
        self.get_infor(buildings.TEACH)


class LiteraBuilding(SpecialBuilding):
    ''' 文科楼 '''
    def __init__(self):
        self.get_infor(buildings.LITERA)


class NorthLib(SpecialBuilding):
    ''' 北图书馆 '''
    def __init__(self):
        self.get_infor(buildings.NORTH)


class SouthLib(SpecialBuilding):
    ''' 南图书馆 '''
    def __init__(self):
        self.get_infor(buildings.SOUTH)


class Gym(SpecialBuilding):
    ''' 体育馆 '''
    def __init__(self):
        self.get_infor(buildings.GYM)


class Classroom(SpecialBuilding):
    ''' 教室 '''
    pass


class Dorm(SpecialBuilding):
    ''' 宿舍 '''
    def __init__(self):
        self.get_infor(buildings.DORM)


class BeingBuilding(SpecialBuilding):
    ''' 正在建设 '''
    def __init__(self):
        self.get_infor(buildings.BEING_BUILT)


class BeingRent(SpecialBuilding):
    """ 出租中 """
    def __init__(self):
        self.get_infor(buildings.RENT)

    def createShop(self, id):
        shop = DbMaster.db.get("SELECT * FROM szu_mu_building WHERE "
                               "id = %s AND special = 'rent'", int(id))
        self.id = shop['id']
        self.title = shop['title']
        self.ownerid = shop['ownerid']
        self.pic = shop['pic']
        self.color = shop['color']
        self.special = shop['special']
        self.descr = shop['descr']

    @staticmethod
    def find(id):
        return find_special(id, 'rent')


special_map = {'office': Office(),
               'northlib': NorthLib(),
               'southlib': SouthLib(),
               'teach': TeachingBuilding(),
               'tech': TechBuilding(),
               'litera': LiteraBuilding(),
               'student': StudentCenter(),
               'stone': Stone(),
               'gym': Gym(),
               'dorm': Dorm(),
               'rent': BeingRent()}
