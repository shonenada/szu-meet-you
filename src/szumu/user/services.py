import os
from hashlib import md5

import tornado
from sqlalchemy.orm import Session

from szumu.user.model import User


session = Session()
query = session.query(User)


def is_username_existed(username):
    """Check if the input username existed in the database."""
    if username is None:
        return None
    count = query.filter_by(username=username).count()
    if count > 0:
        return True
    else:
        return False


def is_nickname_existed(nickname, current_user=None):
    """Check if the input nickname existed in the database."""
    if nickname is None:
        return None
    if current_user is None:
        count = query.filter_by(nickname=nickname).count()
    else:
        count = (query.filter(User.username != current_user)
                      .filter(User.nickname == nickname).count())
    if count > 0:
        return True
    else:
        return False


def is_truename_existed(truename, current_user):
    """Check if the input truename existed in the database."""
    if truename is None or current_user is None:
        return None
    count = (query.filter(User.username != current_user)
                  .filter(User.truename == truename).count())
    if count > 0:
        return True
    else:
        return False


def is_number_existed(number, current_user):
    """Check if the input number existed in the database."""
    if number is None or current_user is None:
        return None
    count = (query.filter(User.username != current_user)
                  .filter(User.number == number).count())
    if count > 0:
        return True
    else:
        return False


def login_validate(username, raw_password):
    """Login action"""
    if username is None or raw_password is None:
        return False
    hashed_password = User.hash_string(User.SALT, raw_password)
    count = (query.filter(User.username == username)
                  .filter(User.hashed_password == hashed_password).count())
    if count > 0:
        return True
    else:
        return False


def find(user_id):
    """Get user by input user id"""
    if user_id is None:
        raise tornado.web.HTTPError(404, 'user_id is None')
    count = query.filter_by(id=user_id).count()
    if count > 0:
        query_user = query.first()
        return query_user
    else:
        return None


def get_user_by_name_and_number(truename, number):
    """ remove? """
    if truename is None or number is None:
        return None
    count = (query.filter_by(truename=truename)
                  .filter_by(number=number).count())
    if count > 0:
        query_user = query.first()
        return query_user
    else:
        return None


def save_user(user):
    """Save user into the database."""
    if not isinstance(user, User):
        return False
    session.add(user)
    session.commit()
    return True


def update_user(user):
    """Update user information"""
    if not isinstance(user, User):
        return False
    this_query = query.filter_by(username=user.username)
    if this_query.count() > 0:
        query_user = this_query.first()
        query_user.nickname = user.nickname
        query_user.truename = user.truename
        query_user.number = user.number
        query_user.college = user.college
        query_user.birthday = user.birthday
        query_user.qq = user.qq
        query_user.state = user.state
        session.commit()
        return True


def get_id_by_username(username):
    if username is None:
        return None
    else:
        query_user = query.filter_by(username=username)
        if query_user.count() > 0:
            return query_user.first().id
        else:
            return None


def get_user_list(page=1, pagesize=20):
    offset = (page - 1) * pagesize
    user_list = this_query = query.offset(offset).limit(pagesize).all()
    return user_list


def get_user_avatar(user_id, avatar_folder='/static/upfiles/avatar/'):
    if user_id is None:
        return None
    else:
        query_user = find(user_id)
        picurl = md5("AvatarUrl:" + str(user_id)).hexdigest()
        pic_path = avatar_folder + picurl + '.png'
        if not os.path.isfile(pic_path):
            if query_user.gender == User.GENDER_MALE:
                picurl = 'male_big'
            else:
                picurl = 'female_big'
        pic_path = avatar_folder + picurl + '.png'
        return pic_path


def add_avatar(user):
    if user is None or not isinstance(user, User):
        return False
    pic_url = get_user_avatar(user.id)
    user.avatar = pic_url
    return True


def with_avatar(user_list):
    for user in user_list:
        add_avatar(user)
