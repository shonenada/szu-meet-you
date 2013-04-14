#-*- coding: utf-8 -*-
import re
import os
import urllib2
import sys

from sqlalchemy.orm import Session

from models import Course


reload(sys)
sys.setdefaultencoding("utf8")

log_file = open("fetch_course.log", "a")

session = Session()
base_url = "http://192.168.240.168/xuanke/coursehtm/"
request_url = base_url + "dept20122.htm"
html_suffix = "20122.htm"
colleges = ['材料学院', '财会学院', '传播学院', '大学英语教学部', '电子科学与技术学院', '法学院', '高尔夫学院', '管理学院', '光电工程学院', '国际交流学院', '化学与化工学院', '机电与控制工程学院', '计算机与软件学院', '建筑与城市规划学院', '教务部()', '经济学院', '社会科学学院', '生命科学学院', '师范学院', '数学与计算科学学院', '体育部', '图书馆', '土木工程学院', '外国语学院', '文化产业研究院', '文学院', '武装部', '物理科学与技术学院', '信息工程学院', '学生部', '医学院', '艺术设计学院', '招生就业办公室', '中国经济特区研究中心']


def fetch_courses():
    key = 1;
    for val in colleges:
        save_path = 'temp/courses/d' + str(key) + "20122.html"
        temp_html_file = open(save_path, 'w')
        url = base_url + "d" + str(key) + html_suffix
        key = key + 1
        response = urllib2.urlopen(url)
        result = response.read().decode('gbk', 'ignore')
        temp_html_file.write(result)
        print "Saved", save_path


def analyse():
    get_tr_pattern = re.compile(r"<tr[\s\S]+?><td><input [\s\S]+?</tr>")
    tr_pattern = re.compile(r"<tr[\s\S]+?><td><input [\s\S]+?></td><td>([\d]+)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td>([\s\S]+?)</td><td><img [\s\S]+?></td><td>([\s\S]*?)</td><td>([\s\S]+?)</td><td>([\s\S]*?)</td><td>([\s\S]*?)</td></tr>")
    for root, dirs, files in os.walk("temp/courses/"):
        for f in files:
            college = f.replace("d", "").replace("l", "").replace(html_suffix, '')
            html_file = open("temp/courses/" + f, 'r')
            html = html_file.read()
            result = tr_pattern.findall(html)
            log_file.write("Saving " + f + "\n")
            print "Saving", f
            save_in_database(result, college)


def save_in_database(info_list, college):
    for info in info_list:
        new_course = Course(info[0].decode('utf-8'), info[1].decode('utf-8'))
        new_course.main_class = info[2].decode('utf-8')
        new_course.teacher = info[3].decode('utf-8')
        new_course.college = college.decode('utf-8')
        new_course.credit = float(info[4].decode('utf-8'))
        new_course.how_to_check = info[5].decode('utf-8')
        new_course.classroom = info[6].decode('utf-8')
        new_course.class_week = info[7].decode('utf-8')
        new_course.score_type = info[8].decode('utf-8')
        new_course.remark = info[9].decode('utf-8')
        session.add(new_course)
        session.commit()


def run():
    fetch_courses()
    analyse()


if __name__ == "__main__":
    run()
