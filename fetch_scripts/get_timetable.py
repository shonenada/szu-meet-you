#-*- coding: utf-8 -*-
import sys

from models import Selection, Timetable, Course, session


reload(sys)
sys.setdefaultencoding("utf8")

hour_time = [1, 2, 3, 4, 5, 6, 7, 8]
hour_str = ['1,2', '3,4', '5,6', '7,8', '5:30-7:00',
            '9,10', '9,10,11', '11,12']
hour_map = dict(zip(hour_str, hour_time))
week_dict = {1: u'(单)', 2: u'(双)'}

stus = [u'黄良兴', u'黄梓桐', u'梁琳', u'潘锦涛', u'张雅思', u'陈东豪',
        u'童芃骏', u'刘宗灵', u'王心', u'李婉玉', u'杨许康', u'郑铭杰']

timetable = [[[], [], [], [], []], [[], [], [], [], []], [[], [], [], [], []],
             [[], [], [], [], []], [[], [], [], [], []], [[], [], [], [], []],
             [[], [], [], [], []], [[], [], [], [], []]]

for stu in stus:

    # Check whether the name is unique
    stu_no = session.query(Selection.stu_no).filter_by(stu_name=stu).all()
    sno = 0
    for no in stu_no:
        if sno == 0:
            sno = no
        if sno != no:
            print no
            print(stu + " is not unique!")
            continue

    courses = (session.query(Selection.course_no, Selection.stu_name)
                      .filter_by(stu_name=stu).all())
    stu_name = courses[0][1]
    for course in courses:
        c_times = (session.query(Timetable.week, Timetable.day,
                                 Timetable.hour, Timetable.course_id)
                          .filter_by(course_id=course[0]).all())
        for c_time in c_times:
            week = c_time[0]
            day = c_time[1]
            hour = c_time[2]
            c_name = (session.query(Course.course_name)
                      .filter_by(course_no=c_time[3]).first())[0]
            text = stu_name + '(' + c_name + ')'
            if week in [1, 2]:
                text = text + week_dict[week]
            timetable[hour_map[hour] - 1][day - 1].append(text)

html = "<html><head><title>Timetable of XXB</title></head><body>"
html = html + "<table border=1><tr><td>课节</td><td>周一</td><td>周二</td>"
html = html + "<td>周三</td><td>周四</td><td>周五</td></tr>"

for i in range(0, 8):
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
