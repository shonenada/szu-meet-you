#-*- coding: utf-8 -*-
import sys

from models import Course, Selection, session


reload(sys)
sys.setdefaultencoding("utf8")


if __name__ == "__main__":

    outfile = open("out.txt", "w")

    student_no = raw_input("student no: ")

    user_selections = (session.query(Selection.course_no)
                      .filter_by(stu_no=student_no))

    for user_selection in user_selections:
        c_no = user_selection.course_no
        selection = (session.query(Selection.stu_name)
                            .filter_by(course_no=c_no))
        course_infor = (session.query(Course.course_name)
                               .filter_by(course_no=c_no)
                               .first())

        outfile.write(course_infor[0] + '\n')
        print course_infor[0]

        courses = (session.query(Selection.stu_name)
                          .filter_by(course_no=c_no)
                          .filter(Selection.stu_no != student_no))

        for course in courses:
            print course[0],
            outfile.write(course[0].encode('utf-8') + '\t')
        print "\n"
        outfile.write('\n')

    raw_input("Press Any key to exit the program.")
