#-*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///courses.sqlite")
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Course(Base):

    __tablename__ = 'courses'
    
    id = Column('id', Integer, primary_key=True)
    course_no = Column('course_no', String(15))
    course_name = Column('course_name', String(150))
    college = Column('college', Integer)
    main_class = Column('main_class', String(150))
    teacher = Column('teacher', String(150))
    credit = Column('credit', Float)
    how_to_check = Column('how_to_check', String(15))
    class_week = Column('class_week', String(10))
    credit_type = Column('credit_type', String(8))
    remark = Column('remark', String(300))

    def __init__(self, course_no, course_name):
        self.course_no = course_no
        self.course_name = course_name


class Selection(Base):

    __tablename__ = 'selections'

    id = Column('id', Integer, primary_key=True)
    course_no = Column('course_no', String(50))
    stu_name = Column('stu_name', String(50))
    stu_no = Column('stu_no', String(10))
    entrance_year = Column('entrance_year', String(2))
    college_no = Column('college_no', String(2))
    gender = Column('gender', Integer)
    major = Column('major', String(50))

    def __init__(self, course_no, name):
        self.course_no = course_no
        self.stu_name = name


class Timetable(Base):

    __tablename__ = 'timetables'

    id = Column('id', Integer, primary_key=True)
    course_id = Column('course_id', String(15))
    week = Column('week', Integer)
    day = Column('day', Integer)
    hour = Column('hour', String(20))
    classroom = Column('classroom', String(30))

    def __init__(self, course_id, week, day, hour, classroom):
        self.course_id = course_id
        self.week = week
        self.day = day
        self.hour = hour
        self.classroom = classroom
