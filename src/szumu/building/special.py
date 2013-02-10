#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16
@author: Lyd
'''

from szumu.building.base import BaseBuilding
from szumu.config import buildings
from szumu.database import DbMaster


db = DbMaster.db


class SpecialBuilding(BaseBuilding):
    """
    Columns:
        1# id
        2# title
        3# ownerid
        4# pic
        5# mapid
        6# mapsite
        7# color
        8# descr
        9# special
    """

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
    '''
    开课单位代号:
        1: 材料学院
        2: 财会学院
        3: 传播学院
        4: 大学英语教学部
        5: 电子科学与技术学院
        6: 法学院
        7: 高等教育研究所
        8: 高尔夫学院
        9: 管理学院
        10:光电工程学院
        11:国际交流学院
        12:化学与化工学院
        13:机电与控制工程学院
        14:计算机与软件学院
        15:建筑与城市规划学院
        16:教务部
        17:经济学院
        18:社会科学学院
        19:生命科学学院
        20:师范学院
        21:数学与计算科学学院
        22:体育部
        23:图书馆
        24:土木工程学院
        25:外国语学院
        26:文学院
        27:武装部
        28:物理科学与技术学院
        29:校团委
        30:信息工程学院
        31:学生部
        32:医学院
        33:艺术设计学院
        34:招生就业办公室
        35:中国经济特区研究中心
    '''

    college_no = buildings.TEACH_COLLEGE_NO

    def __init__(self):
        self.get_infor(buildings.TEACH)

    @staticmethod
    def get_course_infor(id):
        if not DbMaster.db:
            return None
        if not id:
            return None
        return DbMaster.db.get('SELECT * FROM `szu_mu_course` WHERE id=%s',
                               int(id))

    @staticmethod
    def get_course_infor_by_classid(classid):
        if not DbMaster.db:
            return None
        if not classid:
            return None
        return DbMaster.db.get('SELECT * FROM `szu_mu_course` WHERE cid = %s',
                               int(classid))

    @staticmethod
    def get_class_infor_by_truename_and_number(truename, number):
        if not DbMaster.db:
            return None
        if not truename:
            return None
        if not number:
            return None
        return DbMaster.db.query("SELECT * FROM `szu_mu_stuselect` WHERE "
                                 "truename = %s and number = %s",
                                 truename, number)

    @staticmethod
    def get_class_infor_by_classid(classid):
        if not DbMaster.db:
            return None
        if not classid:
            return None
        return DbMaster.db.query("SELECT * FROM `szu_mu_stuselect` "
                                 "WHERE cid = %s", classid)


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

    def save(self):
        if not DbMaster.db:
            return None
        if not self.id:
            return None

        return DbMaster.db.execute("UPDATE `szu_mu_building` SET "
                                   "title = %s, ownerid = %s, special = %s, "
                                   "descr = %s WHERE id = %s ",
                                   self.title, int(self.ownerid),
                                   self.special, self.descr, int(self.id))

    @staticmethod
    def find(id):
        if not id:
            return None
        return DbMaster.db.get("SELECT * FROM szu_mu_building WHERE "
                               "id = %s AND special = 'rent'", int(id))


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


class ClassComment():
    ''' 课程评价 '''
    """
        TableName = 'szu_mu_class_comment'
        Columns:
            1# id
            2# classid
            3# userid
            4# comment
            5# created
    """

    id = None
    classid = None
    userid = None
    comment = None
    created = None

    def __init__(self, classid, userid, comment):
        self.classid = classid
        self.userid = userid
        self.comment = comment

    def save(self):
        if not self.classid:
            return None
        if not self.userid:
            return None
        if not self.comment:
            return None

        return DbMaster.db.execute("INSERT INTO `szu_mu_class_comment` "
                                   "(classid, userid, comment) "
                                   "VALUES(%s, %s, %s)",
                                   self.classid, self.userid, self.comment)

    @staticmethod
    def get_comment_by_classid(classid):
        if not classid:
            return None
        return DbMaster.db.query('SELECT * FROM `szu_mu_class_comment` WHERE '
                                 'classid = %s ORDER BY id DESC', classid)
