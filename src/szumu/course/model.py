#/usr/bin/env python
#-*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import mapper, Session

from szumu.database import metadata


session = Session()


class Course(object):

    def __init__(self, cid, classname):
        self.cid = cid
        self.classname = classname


class StuSelect(object):

    def __init__(self, number, truename, cid):
        self.number = number
        self.truename = truename
        self.cid = cid


class Comment(object):

    def __init__(self, classid, userid, comment):
        self.classid = classid
        self.userid = userid
        self.comment = comment


course_table = Table('course', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('cid', Integer),
                     Column('classname', String(50)),
                     Column('teacher', String(50)),
                     Column('college', Integer),
                     Column('mainclass', String(100)),
                     Column('classroom', String(100)),
                     Column('mark', Float),
                     Column('checktype', String(5)),
                     Column('learnhour', String(10)),
                     Column('mark_type', String(20)),
                     Column('remark', String(255))
                     )

stuselect_table = Table('stuselect', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('number', Integer),
                        Column('truename', String(20)),
                        Column('gender', String(1)),
                        Column('major', String(20)),
                        Column('cid', Integer)
                        )

comment_table = Table('comment', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('classid', Integer),
                      Column('userid', Integer),
                      Column('comment', String),
                      Column('created', DateTime, default=datetime.now())
                     )


mapper(Course, course_table)
mapper(StuSelect, stuselect_table)
mapper(Comment, comment_table)
