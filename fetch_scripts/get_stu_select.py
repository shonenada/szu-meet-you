#-*- coding: utf-8 -*-

import re
import os
import json
import urllib2
import sys
from urllib import urlencode

from bs4 import BeautifulSoup

from models import Selection, Course, session


reload(sys)
sys.setdefaultencoding("utf8")

log_file = open("stu_select.log", "a")

cookie_url = "http://192.168.2.229/newkc/akcjj0.asp?xqh=20122"
headers = {}
GENDER = {u'男': 1, u'女': 0}


def setup_cookie():
    global headers
    request = urllib2.urlopen(cookie_url)
    cookie_pattern = re.compile(r"Set-Cookie: (\S+?);")
    result = cookie_pattern.findall(str(request.info()))
    headers = {'Cookie': result[0]}


def get_infor(classid):
    req = urllib2.Request("http://192.168.2.229/newkc/kcxkrs.asp?ykch=" +
                          str(classid), headers=headers)
    r = urllib2.urlopen(req)
    html = r.read().decode('gbk', 'ignore')
    return html


def save_html(html, classid):
    html_file = open("temp/selections/" + str(classid) + ".html", 'w')
    html_file.write(html)
    log_file.write("Saved" + "temp/selections/" + str(classid) + ".html\n")
    print "Saved temp/selections/" + str(classid) + ".html"


def read_html(html, classid):
    if len(html) > 1800:
        analyse(html, classid)
    else:
        log_file.write(str(classid) + ' is not a invalid file!')


def read_temp_html():
    for root, dirs, files in os.walk("temp/selections/"):
        for f in files:
            html_file = open("temp/selections/" + f, 'r')
            html = html_file.read()
            if len(html) > 1800:
                analyse(html, f.replace('.html', ''))
            else:
                log_file.write(f + 'is a invalid file!')


def analyse(html, classid):
    soup = BeautifulSoup(html)
    first_table = soup.table
    first_table.extract()
    first_tr = soup.tr
    first_tr.extract()
    tr_list = soup.findAll('tr')
    tr_pattern = re.compile(r"<tr><td>\d+</td><td>(\d+)</td><td>(\S+?)</td><td>(\S+?)</td><td><small>(\S+?)</small></td></tr>")
    for tr in tr_list:
        if tr:
            tr = str(tr).replace('\n', '').replace(' ', '')
            info = tr_pattern.findall(tr)[0]
            log_file.write("Getting" + " " + str(classid) + " " +
                           str(info[0]) + '\n')
            print "Getting" + " " + str(classid) + " " + str(info[0])
            save_in_database(info, classid)


def save_in_database(info, classid):
    new_stu = Selection(classid, info[1].decode('utf-8'))
    new_stu.entrance_year = info[0][2:4]
    new_stu.college_no = info[0][4:6]
    new_stu.stu_no = info[0]
    new_stu.gender = GENDER[info[2].decode('utf-8')]
    new_stu.major = info[3].decode('utf-8')
    session.add(new_stu)


def fetch_html():
    setup_cookie()
    courses = session.query(Course).all()
    for course in courses:
        c_no = course.course_no
        html = get_infor(c_no)
        read_html(html, c_no)


def selection_analyse():
    fetch_html()
    # read_temp_html()
    session.commit()
