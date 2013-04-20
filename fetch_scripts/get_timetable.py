#-*- coding: utf-8 -*-
import sys

from models import Selection, Timetable, session


reload(sys)
sys.setdefaultencoding("utf8")

hour_time =[1, 2, 3, 4, 5, 6]
hour_str = ['1,2', '3,4', '5,6', '7,8', '9,10', '11,12']
hour_map = dict(zip(hour_str, hour_time))
week_dict = {1: u'(单)', 2: u'(双)'}

stus = []

timetable = [[[], [], [], [], []], [[], [], [], [], []], [[], [], [], [], []],
             [[], [], [], [], []], [[], [], [], [], []], [[], [], [], [], []]]

for stu in stus:
    courses = (session.query(Selection.course_no, Selection.stu_name)
                      .filter_by(stu_no=stu).all())
    stu_name = courses[0][1]
    for course in courses:
        c_times = (session.query(Timetable.week, Timetable.day, Timetable.hour)
                         .filter_by(course_id=course[0]).all())
        for c_time in c_times:
            week = c_time[0]
            day = c_time[1]
            hour = c_time[2]
            text = stu_name
            if week in [1, 2]:
                text = text + week_dict[week]
            timetable[hour_map[hour] - 1][day - 1].append(text)

html = "<html><head><title>Timetable of XXB</title></head><body>"
html = html + "<table border=1><tr><td>课节</td><td>周一</td><td>周二</td>"
html = html + "<td>周三</td><td>周四</td><td>周五</td></tr>"

for i in range(0, 6):
    html = html + "<tr><td>" + str(hour_str[i]) + "</td>"
    for j in range(0, 5):
        html = html + "<td>"
        if timetable[i][j]:
            for stu in timetable[i][j]:
                html = html + stu + "<br />"
        html = html + "</td>"
    html = html + "</tr>"

html = html + "</body></html>"
f = open("out.html", 'w')
f.write(html)   
