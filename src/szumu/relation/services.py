from sqlalchemy.orm import Session

from szumu.relation.model import Relation

session = Session()
query = session.query(Relation)


def get_focus_list(user_id):
    if user_id is None:
        return None
    else:
        focus_list = (query.filter_by(fromid=user_id)
                           .filter_by(relation=Relation.FOCUS).all())
        return focus_list


def get_ignore_list(user_id):
    if user_id is None:
        return None
    else:
        ignore_list = (query.filter_by(fromid=user_id)
                            .filter_by(relation=Relation.IGNORE)
                            .all())
        return ignore_list


def get_being_focused_list(user_id):
    if user_id is None:
        return None
    else:
        focused_list = (query.filter_by(toid=user_id)
                             .filter_by(relation=Relation.FOCUS)
                             .all())
        return focused_list


def get_being_ignored_list(user_id):
    if user_id is None:
        return None
    else:
        ignored_list = (query.filter_by(toid=user_id)
                             .filter_by(relation=Relation.IGNORE)
                             .all())
        return ignored_list


def get_each_friend_list(user_id):
    focus_list = get_focus_list(user_id)
    focused_list = get_being_focused_list(user_id)
    focused_id_list = []
    friends = []
    for focused in focused_list:
        focused_id_list.append(focused.fromid)
    for focus in focus_list:
        if focus.toid in focused_list:
            friends.append(focus.toid)
    return friends


def is_my_friend(user_id, friend_id):
    is_my_friend = (query.filter_by(fromid=user_id)
                         .filter_by(toid=friend_id)
                         .filter_by(relation=Relation.FOCUS))
    count = is_friend.count()
    if count > 0:
        return True
    else:
        return False


def is_each_friend(one_id, two_id):
    is_my_friend = (query.filter_by(fromid=one_id)
                         .filter_by(toid=two_id)
                         .filter_by(relation=Relation.FOCUS)
                         .count() > 0)
    is_his_friend = (query.filter_by(fromid=two_id)
                          .filter_by(toid=one_id)
                          .filter_by(relation=Relation.FOCUS)
                          .count() > 0)
    return (is_my_friend and is_his_friend)


def save_relation(relation):
    if not isinstance(relation, Relation):
        return False
    else:
        session.add(relation)
        session.commit()
        return True


def remove_relation(relation):
    if not isinstance(relation, Relation):
        return False
    else:
        session.delete(relation)
        session.commit()
        return True


def get_relation(my_id, other_id):
    if not my_id or not other_id:
        return None
    else:
        this_query = query.filter_by(fromid=my_id).filter_by(toid=other_id)
        if this_query.count() > 0:
            return this_query.first()
        else:
            return None


def with_relation(current_user_id, user_list):
    for user in user_list:
        relation = get_relation(current_user_id, user.id)
        user.relation = relation
