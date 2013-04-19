#-*- coding: utf-8 -*-
import sys

from sqlalchemy.orm import Session

from models import Course, Selections


reload(sys)
sys.setdefaultencoding("utf8")

session = Session()


if __name__ == "__main__":

    outfile = open("out.txt", "w")

    student_no = raw_input("student no: ")

    user_selections = (session.query(Selections.course_no)
                      .filter_by(uid=student_no))

    for user_selection in user_selections:
        c_no = user_selection.course_no
        selection = (session.query(Selections.name)
                            .filter_by(course_no=c_no))
        course_infor = (session.query(Course.course_name)
                               .filter_by(course_no=c_no)
                               .first())

        outfile.write(course_infor[0] + '\n')

        courses = (session.query(Selections.name)
                          .filter_by(course_no=c_no)
                          .filter(Selections.uid != student_no))

        for course in courses:
            outfile.write(course.name + '\t')
        outfile.write('\n')
