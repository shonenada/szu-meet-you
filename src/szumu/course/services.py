from sqlalchemy.orm import Session

from szumu.course.model import Course, StuSelect, Comment


session = Session()
course_query = session.query(Course)
comment_query = session.query(Comment)
stuselect_query = session.query(StuSelect)


def find(id):
    if id is None or not isinstance(id, int):
        return None
    else:
        query_course = course_query.filter_by(id=id)
        if query_course.count() > 0:
            return query_course.first()
        else:
            return None
        return None


def find_by_classid(classid):
    if classid is None or not isinstance(classid, int):
        return None
    else:
        query_course = course_query.filter_by(cid=classid)
        if query_course.count() > 0:
            return query_course.first()
        else:
            return None
        return None


def find(id):
    if id is None or not isinstance(id, int):
        return None
    else:
        query_comment = comment_query.filter_by(id=id)
        if query_comment.count() > 0:
            return query_comment.first()
        else:
            return None
        return None


def find_by_classid(classid):
    if classid is None or not isinstance(classid, int):
        return None
    else:
        query_comment = comment_query.filter_by(cid=classid)
        if query_comment.count() > 0:
            return query_comment.first()
        else:
            return None
        return None


def save_comment(comment):
    if comment is None or not isinstance(comment, Comment):
        return False
    else:
        session.add(comment)
        session.commit()
        return True


def get_stu_select_by_name_and_number(truename, number):
    if truename is None or number is None:
        return None
    query_stu_select = (stuselect_query.filter_by(truename=truename)
                                       .filter_by(number=number))
    if query_stu_select.count() > 0:
        return query_stu_select.all()
    else:
        return None


def get_stu_select_by_classid(classid):
    if classid is None or not isinstance(classid, int):
        return None
    else:
        query_stu_select = query_stu_select.filter_by(cid=classid)
        if query_stu_select.count() > 0:
            return query_stu_select.all()
        else:
            return None
