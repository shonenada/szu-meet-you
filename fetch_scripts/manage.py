#-*- coding: utf-8 -*-

from models import Course, Selection, Timetable, Base, engine
from fetch_course import fetch_courses
# from get_stu_select import selection_analyse


def run():
    Base.metadata.create_all(engine)        # Create database and tables
    fetch_courses()         # Fetch information from url
    # selection_analyse()     # Analyse selections


if __name__ == "__main__":
    run()
