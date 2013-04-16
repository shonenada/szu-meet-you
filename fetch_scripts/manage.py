#-*- coding: utf-8 -*-

from sqlalchemy.orm import Session

from models import metadata
from fetch_course import fetch_courses
from get_stu_select import selection_analyse


session = Session()


if __name__ == "__main__":
    metadata.create_all()
    fetch_courses()
    selection_analyse()
