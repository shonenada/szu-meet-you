#-*- coding: utf-8 -*-
import re
import os
import urllib2
import sys

from sqlalchemy.orm import Session

from models import Course, Timetable


reload(sys)
sys.setdefaultencoding("utf8")

log_file = open("fetch_course.log", "a")

session = Session()

base_url = "http://192.168.240.168/xuanke/coursehtm/"
request_url = base_url + "dept20122.htm"
html_suffix = "20122.htm"

colleges = ['材料学院', '财会学院', '传播学院', '大学英语教学部', '电子科学与技术学院', '法学院', '高尔夫学院', '管理学院', '光电工程学院', '国际交流学院', '化学与化工学院', '机电与控制工程学院', '计算机与软件学院', '建筑与城市规划学院', '教务部()', '经济学院', '社会科学学院', '生命科学学院', '师范学院', '数学与计算科学学院', '体育部', '图书馆', '土木工程学院', '外国语学院', '文化产业研究院', '文学院', '武装部', '物理科学与技术学院', '信息工程学院', '学生部', '医学院', '艺术设计学院', '招生就业办公室', '中国经济特区研究中心']

list_pattern = re.compile("([\S]+?)(\d+(?:,\d+){1,2})\(([\S].*)\)")
special_pattern = re.compile("([\S]+?)(\d+:\d+-\d+:\d+)\((\S+?)\(\S+?\)\)")
get_tr_pattern = re.compile(r"<tr[\s\S]+?><td><input [\s\S]+?</tr>")
tr_pattern = re.compile(r"<tr[\s\S]+?><td><input [\s\S]+?></td><td>([\d]+)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td><img [\s\S]+?></td><td>([\s\S]*?)</td><td>([\s\S]+?)</td><td>([\s\S]*?)</td><td>([\s\S]*?)</td></tr>")

day_dict = {u"一": 1, u"二": 2, u"三": 3, u"四": 4, u"五": 5}
week_dict = {u"周": 0, u"单": 1, u"双": 2}


def read_url():
    key = 1;
    for val in colleges:
        url = base_url + "d" + str(key) + html_suffix
        key = key + 1
        response = urllib2.urlopen(url)
        result = response.read().decode('gbk', 'ignore')
        log_file.write("Fetching from " + url + "\n")
        print "Fetching from " + url + "\n"
        analyse(result, key)


def analyse(html, college):
    result = tr_pattern.findall(html)
    log_file.write("Saving\n")
    print "Saving"
    save_in_database(result, college)


def save_in_database(info_list, college):
    for info in info_list:
        new_course = Course(info[0].decode('utf-8'), info[1].decode('utf-8'))
        new_course.main_class = info[2].decode('utf-8')
        new_course.teacher = info[3].replace('()', '').decode('utf-8')
        new_course.college = college
        new_course.credit = float(info[4].decode('utf-8'))
        new_course.how_to_check = info[5].decode('utf-8')
        new_course.class_week = info[7].decode('utf-8')
        new_course.credit_type = info[8].decode('utf-8')
        new_course.remark = info[9].decode('utf-8')

        classrooms = info[6].split(';')
        for classroom in classrooms:
            regrex_result = list_pattern.findall(classroom)
            special_result = special_pattern.findall(classroom)
            if regrex_result:
                day = day_dict[regrex_result[0][0][-1]]
                week = week_dict[regrex_result[0][0][0:1]]
                hour = regrex_result[0][1]
                classroom = regrex_result[0][2]
            if special_result:
                day = day_dict[special_result[0][0][-1]]
                week = week_dict[special_result[0][0][0:1]]
                hour = special_result[0][1]
                classroom = special_result[0][2]
            timetable = Timetable(info[0].decode('utf-8'), week, day, hour, classroom.decode('utf-8'))
            session.add(timetable)
        log_file.write("Saved\n")
        print "Saved"
        session.add(new_course)


def fetch_courses():
    read_url()
    session.commit()
