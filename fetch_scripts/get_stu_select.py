#-*- coding: utf-8 -*-

import re
import os
import json
import urllib2
import sys
from urllib import urlencode

from sqlalchemy.orm import Session
from bs4 import BeautifulSoup

from models import StuSelect, Course


reload(sys)
sys.setdefaultencoding("utf8")

log_file = open("stu_select.log", "a")

session = Session()
cookie_url = "http://192.168.2.229/newkc/akcjj0.asp?xqh=20122"
headers = {}


def setup_cookie():
    global headers
    request = urllib2.urlopen(cookie_url)
    cookie_pattern = re.compile(r"Set-Cookie: (\S+?);")
    result = cookie_pattern.findall(str(request.info()))
    headers = {'Cookie': result[0]}


def get_infor(classid):
    req = urllib2.Request("http://192.168.2.229/newkc/kcxkrs.asp?ykch=" + str(classid), headers=headers)
    r = urllib2.urlopen(req)
    html = r.read().decode('gbk', 'ignore')
    return html


def save_html(html, classid):
    html_file = open("temp/" + str(classid) + ".html", 'w')
    html_file.write(html)
    print "Saved", "temp/" + str(classid) + ".html"


def read_temp_html():
    for root, dirs, files in os.walk("temp/"):
        for f in files:
            html_file = open("temp/" + f, 'r')
            analyse(html_file.read(), f.replace('.html', ''))



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
            log_file.write("Getting" +  " " + str(classid) + " " + str(info[0]) + '\n')
            print("Getting" +  " " + str(classid) + " " + str(info[0]) + '\n')
            save_in_database(info, classid)


def save_in_database(info, classid):
    new_stu = StuSelect(classid, info[1].decode('utf-8'))
    new_stu.uid = info[0].decode('utf-8')
    new_stu.gender = info[2].decode('utf-8')
    new_stu.major = info[3].decode('utf-8')
    session.add(new_stu)
    session.commit()


def fetch_html():
    setup_cookie()
    courses = session.query(Course).all()
    for course in courses:
        c_no = course.course_no
        html = get_infor(c_no)
        save_html(html, c_no)


def run():
    fetch_html()
    read_temp_html()
    

if __name__ == "__main__":
    run()
