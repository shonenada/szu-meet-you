#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-16
@author: Lyd
'''
class buildingConfig(object):
    
    szumu_building_office = {'title':'办公楼',
                             'ownerid':0,
                             'pic':None,
                             'mapid':0,
                             'mapsite':0,
                             'descr':"深大觅友社区办公楼，处理社区各类事务",
                             'color':'brown',
                             'special':'office',
                             }
    
    szumu_building_student_center = {'title':'学生活动中心',
                                     'ownerid':0,
                                     'pic':None,
                                     'mapid':0,
                                     'mapsite':0,
                                     'descr':"学生活动中心，提供各社团信息",
                                     'color':'brown',
                                     'special':'student',
                                     }
    
    szumu_building_stone = {'title':'石头坞',
                             'ownerid':0,
                             'pic':None,
                             'mapid':0,
                             'mapsite':0,
                             'descr':"石头坞，昔日的乐园",
                             'color':'brown',
                             'special':'stone',
                             }
    
    szumu_building_tech = {'title':'科技楼',
                             'ownerid':0,
                             'pic':None,
                             'mapid':0,
                             'mapsite':0,
                             'descr':"深大觅友社区的实验室",
                             'color':'brown',
                             'special':'tech',
                             }
    
    szumu_building_teach = {'title':'教学楼',
                             'ownerid':0,
                             'pic':None,
                             'mapid':0,
                             'mapsite':0,
                             'descr':"教学楼，寻觅你的未曾见面的老朋友",
                             'color':'brown',
                             'special':'teach',
                             }
    
    szumu_building_litera = {'title':'文科楼',
                             'ownerid':0,
                             'pic':None,
                             'mapid':0,
                             'mapsite':0,
                             'descr':"传承深大文化",
                             'color':'brown',
                             'special':'litera',
                             }
    
    szumu_building_north = {'title':'图书馆北馆',
                             'ownerid':0,
                             'pic':None,
                             'mapid':0,
                             'mapsite':0,
                             'descr':"记载深大觅友社区的点滴历史",
                             'color':'brown',
                             'special':'north',
                             }
    
    szumu_building_south = {'title':'图书馆南馆',
                             'ownerid':0,
                             'pic':None,
                             'mapid':0,
                             'mapsite':0,
                             'descr':"闻书香，识友人",
                             'color':'brown',
                             'special':'south',
                             }
    
    szumu_building_gym = {'title':'体育馆',
                          'ownerid':0,
                          'pic':None,
                          'mapid':0,
                          'mapsite':0,
                          'descr':"运动造就人脉",
                          'color':'brown',
                          'special':'gym',
                          }
    
    szumu_building_rent = {'title':'出租中',
                          'ownerid':0,
                          'pic':None,
                          'mapid':0,
                          'mapsite':0,
                          'descr':"出租中。。。",
                          'color':'brown',
                          'special':'sold',
                          }
    
    szumu_building_dorm = {'title':'学生宿舍',
                           'ownerid':0,
                           'pic':None,
                           'mapid':0,
                           'mapsite':0,
                           'descr':"学生宿舍",
                           'color':'brown',
                           'special':'dorm',
                           }
    
    szumu_building_beingBuilt = {
                            'title':'正在建设',
                            'ownerid':0,
                            'pic':None,
                            'mapid':0,
                            'mapsite':0,
                            'descr':'正在建设...',
                            'color':'brown',
                            'special':'beingBuilt',
                            }
    
    
    

    """ 出租店铺类型 """
    szumu_building_rent_type = [
                                {'id':'shop/private', 'name':'个人店铺',},
                                {'id':'shop/topic', 'name':'主题店铺',},
                                {'id':'shop/sell', 'name':'商品店铺',}
                               ]
    
    """ 开课单位代号（ 每学期需要更新一次） """
    szumu_building_teach_college_no = {
                                         1: '材料学院', 
                                         2: '财会学院', 
                                         3: '传播学院',
                                         4: '大学英语教学部',
                                         5: '电子科学与技术学院',
                                         6: '法学院',
                                         7: '高等教育研究所',
                                         8: '高尔夫学院',
                                         9: '管理学院',
                                         10:'光电工程学院',
                                         11:'国际交流学院',
                                         12:'化学与化工学院',
                                         13:'机电与控制工程学院',
                                         14:'计算机与软件学院',
                                         15:'建筑与城市规划学院',
                                         16:'教务部',
                                         17:'经济学院',
                                         18:'社会科学学院',
                                         19:'生命科学学院',
                                         20:'师范学院',
                                         21:'数学与计算科学学院',
                                         22:'体育部',
                                         23:'图书馆',
                                         24:'土木工程学院',
                                         25:'外国语学院',
                                         26:'文学院',
                                         27:'武装部',
                                         28:'物理科学与技术学院',
                                         29:'校团委',
                                         30:'信息工程学院',
                                         31:'学生部',
                                         32:'医学院',
                                         33:'艺术设计学院',
                                         34:'招生就业办公室',
                                         35:'中国经济特区研究中心',
                                        }
    