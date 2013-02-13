#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session


class DbMaster():

    engine = None
    metadata = None

    def init_app(self, app, connect=True):
        self.app = app
        if connect:
            self.connect()

    def connect(self):
        self.engine = create_engine(self.app.config['db_uri'])
        self.metadata = MetaData(self.engine)
        DbMaster.engine = self.engine
        DbMaster.metadata = self.metadata


dbmaster = DbMaster()
metadata = DbMaster.metadata


def import_tables():
    from szumu.user.model import user_table
    from szumu.relationship.model import relationship_table
    from szumu.message.model import message_table
    from szumu.course.model import comment_table, course_table, stuselect_table
    from szumu.map.model import map_table
    from szumu.building.base import building_table
    from szumu.article.model import article_table


def create_table():
    import_tables()
    DbMaster.metadata.create_all()
    init_table()


def init_table():
    import_tables()
    init_map()


def init_map():
    from szumu.map.model import Map
    map1 = Map('first', '深大觅友社区的第一张地图。是一个神秘的地带，进入此地，你将永远出不去。人称“死胡同”')
    map1.path = '1,1,1,1'
    map1.link = '17,18,0,16'
    map1.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map1.created = '0000-00-00 00:00:00'

    map2 = Map('办公楼附近', '办公楼附近')
    map2.path = '1,1,1,1'
    map2.link = '17,18,0,16'
    map2.buildings = 'None,None,None,office,None,None,None,None,None,None,None,None,None,None'
    map2.created = '0000-00-00 00:00:00'

    map3 = Map('图书馆北馆附近', '图书馆北馆附近') 
    map3.path = '1,1,1,1'
    map3.link = '10,20,17,9'
    map3.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,northlib,None'
    map3.created = '0000-00-00 00:00:00'

    map4 = Map('图书馆南馆附近', '图书馆南馆附近') 
    map4.path = '0,1,1,1'
    map4.link = '0,11,10,12'
    map4.buildings = 'None,southlib,None,None,None,None,None,None,None,None,None,None,None,None'
    map4.created = '0000-00-00 00:00:00'

    map5 = Map('教学楼附近', '教学楼附近') 
    map5.path = '1,1,1,1'
    map5.link = '21,26,22,11'
    map5.buildings = 'None,teach,None,None,None,None,None,None,None,None,None,None,None,None'
    map5.created = '0000-00-00 00:00:00'

    map6 = Map('科技楼附近', '科技楼附近') 
    map6.path = '1,1,1,0'
    map6.link = '14,9,15,0'
    map6.buildings = 'None,None,None,None,None,None,tech,None,None,None,None,None,None,None'
    map6.created = '0000-00-00 00:00:00'

    map7 = Map('文科楼附近', '文科楼附近') 
    map7.path = '1,1,0,0'
    map7.link = '15,16,0,0'
    map7.buildings = 'None,None,None,None,None,None,None,None,None,None,litera,None,None,None'
    map7.created = '0000-00-00 00:00:00'

    map8 = Map('学生活动中心附近', '学生活动中心附近') 
    map8.path = '0,0,1,1'
    map8.link = '0,0,24,25'
    map8.buildings = 'None,None,None,student,None,None,None,None,None,None,None,None,None,None'
    map8.created = '0000-00-00 00:00:00'

    map9 = Map('小路', '北馆与科技楼之间的小路') 
    map9.path = '0,1,0,1'
    map9.link = '0,3,0,6'
    map9.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map9.created = '0000-00-00 00:00:00'

    map10 = Map('小路', '南馆与北馆之间小路') 
    map10.path = '1,0,1,0'
    map10.link = '4,0,3,0'
    map10.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map10.created = '0000-00-00 00:00:00'

    map11 = Map('小路', '南馆与教学楼之间小路') 
    map11.path = '0,1,0,1'
    map11.link = '0,5,0,4'
    map11.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map11.created = '0000-00-00 00:00:00'

    map12 = Map('小路', '南馆与元平体育场之间小路') 
    map12.path = '0,1,0,1'
    map12.link = '0,4,0,13'
    map12.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map12.created = '0000-00-00 00:00:00'

    map13 = Map('元平体育场附近', '元平体育场附近') 
    map13.path = '0,1,1,0'
    map13.link = '0,12,14,0'
    map13.buildings = 'None,gym,None,None,None,None,None,None,None,None,None,None,None,None'
    map13.created = '0000-00-00 00:00:00'

    map14 = Map('小路', '元平体育场与科技楼之间的小路') 
    map14.path = '1,0,1,0'
    map14.link = '13,0,6,0'
    map14.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map14.created = '0000-00-00 00:00:00'

    map15 = Map('小路', '科技楼与文科楼之间的小路') 
    map15.path = '1,0,1,0'
    map15.link = '6,0,7,0'
    map15.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map15.created = '0000-00-00 00:00:00'

    map16 = Map('小路', '文科楼与办公楼之间的小路') 
    map16.path = '0,1,0,1'
    map16.link = '0,2,0,7'
    map16.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map16.created = '0000-00-00 00:00:00'

    map17 = Map('小路', '办公楼与北馆之间的小路') 
    map17.path = '1,0,1,0'
    map17.link = '3,0,2,0'
    map17.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map17.created = '0000-00-00 00:00:00'

    map18 = Map('小路', '办公楼与学生宿舍区之间的小路') 
    map18.path = '0,1,0,1'
    map18.link = '0,27,0,2'
    map18.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map18.created = '0000-00-00 00:00:00'

    map19 = Map('学生宿舍区', '学生宿舍区') 
    map19.path = '1,0,1,1'
    map19.link = '22,0,23,20'
    map19.buildings = 'None,None,None,None,None,None,None,dorm,None,None,None,None,None,None'
    map19.created = '0000-00-00 00:00:00'

    map20 = Map('小路', '北馆到学生宿舍区之间的小路') 
    map20.path = '0,1,0,1'
    map20.link = '0,19,0,3'
    map20.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map20.created = '0000-00-00 00:00:00'

    map21 = Map('小路', '教学楼与学生活动中心之间的小路') 
    map21.path = '1,0,1,0'
    map21.link = '28,0,5,0'
    map21.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map21.created = '0000-00-00 00:00:00'

    map22 = Map('小路', '学生宿舍区与教学楼之间的小路') 
    map22.path = '1,0,1,0'
    map22.link = '5,0,19,0'
    map22.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map22.created = '0000-00-00 00:00:00'

    map23 = Map('小路', '办公楼与学生宿舍区之间的小路') 
    map23.path = '1,0,1,0'
    map23.link = '19,0,27,0'
    map23.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map23.created = '0000-00-00 00:00:00'

    map24 = Map('石头坞附近', '石头坞附近') 
    map24.path = '1,0,0,1'
    map24.link = '8,0,0,26'
    map24.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,stone,None'
    map24.created = '0000-00-00 00:00:00'

    map25 = Map('小路', '教学楼与学生活动中心之间的小路') 
    map25.path = '0,1,0,1'
    map25.link = '0,8,0,28'
    map25.buildings = '11,None,12,None,None,None,None,None,None,None,None,None,None,None'
    map25.created = '0000-00-00 00:00:00'

    map26 = Map('小路', '教学楼与石头坞之间的小路') 
    map26.path = '0,1,0,1'
    map26.link = '0,24,0,5'
    map26.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map26.created = '0000-00-00 00:00:00'

    map27 = Map('拐角', '办公楼到学生宿舍区之间的拐角') 
    map27.path = '1,0,0,1'
    map27.link = '23,0,0,18'
    map27.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map27.created = '0000-00-00 00:00:00'

    map28 = Map('拐角', '教学楼与学生活动中心之间的拐角') 
    map28.path = '0,1,1,0'
    map28.link = '0,25,21,0'
    map28.buildings = 'None,None,None,None,None,None,None,None,None,None,None,None,None,None'
    map28.created = '0000-00-00 00:00:00'

    session = Session()

    session.add(map1)
    session.add(map2)
    session.add(map3)
    session.add(map4)
    session.add(map5)
    session.add(map6)
    session.add(map7)
    session.add(map8)
    session.add(map9)
    session.add(map10)
    session.add(map11)
    session.add(map12)
    session.add(map13)
    session.add(map14)
    session.add(map15)
    session.add(map16)
    session.add(map17)
    session.add(map18)
    session.add(map19)
    session.add(map20)
    session.add(map21)
    session.add(map22)
    session.add(map23)
    session.add(map24)
    session.add(map25)
    session.add(map26)
    session.add(map27)
    session.add(map28)
    session.commit()