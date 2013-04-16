from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import mapper


engine = create_engine("sqlite:///courses.sqlite")
metadata = MetaData(engine)


class Course(object):
    def __init__(self, course_no, course_name):
        self.course_no = course_no
        self.course_name = course_name


class StuSelect(object):
    def __init__(self, course_no, name):
        self.course_no = course_no
        self.name = name


class Timetable(object):
    def __init__(self, course_id, week, day, hour, classroom):
        self.course_id = course_id
        self.week = week
        self.day = day
        self.hour = hour
        self.classroom = classroom


course_table = Table("courses", metadata,
                     Column('id', Integer, primary_key=True),
                     Column('course_no', String(15)),
                     Column('course_name', String(150)),
                     Column('college', Integer),
                     Column('main_class', String(150)),
                     Column('teacher', String(150)),
                     Column('credit', Float),
                     Column('how_to_check', String(15)),
                     Column('class_week', String(10)),
                     Column('credit_type', String(8)),
                     Column('remark', String(300))
                     )

select_table = Table('selects', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('course_no', String(50)),
                     Column('name', String(50)),
                     Column('uid', String(20)),
                     Column('gender', String(10)),
                     Column('major', String(50))
                     )

timetable_table = Table('timetable', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('course_id', String(15)),
                        Column('week', Integer),
                        Column('day', Integer),
                        Column('hour', String(20)),
                        Column('classroom', String(30))
                        )


mapper(Course, course_table)
mapper(StuSelect, select_table)
mapper(Timetable, timetable_table)
