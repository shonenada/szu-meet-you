from sqlalchemy.orm import Session

from szumu.relationship.model import RelationShip

session = Session()
query = session.query(RelationShip)


def get_focus_list(user_id):
    if user_id is None:
        return None
    else:
        focus_list = (query.filter_by(fromid=user_id)
                           .filter_by(relationship=RelationShip.FOCUS).all())
        return focus_list


def get_ignore_list(user_id):
    if user_id is None:
        return None
    else:
        ignore_list = (query.filter_by(fromid=user_id)
                            .filter_by(relationship=RelationShip.IGNORE)
                            .all())
        return ignore_list


def get_being_focused_list(user_id):
    if user_id is None:
        return None
    else:
        focused_list = (query.filter_by(toid=user_id)
                             .filter_by(relationship=RelationShip.FOCUS)
                             .all())
        return focused_list


def get_being_ignored_list(user_id):
    if user_id is None:
        return None
    else:
        ignored_list = (query.filter_by(toid=user_id)
                             .filter_by(relationship=RelationShip.IGNORE)
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
                         .filter_by(relationship=RelationShip.FOCUS))
    count = is_friend.count()
    if count > 0:
        return True
    else:
        return False


def is_each_friend(one_id, two_id):
    is_my_friend = (query.filter_by(fromid=one_id)
                         .filter_by(toid=two_id)
                         .filter_by(relationship=RelationShip.FOCUS)
                         .count() > 0)
    is_his_friend = (query.filter_by(fromid=two_id)
                          .filter_by(toid=one_id)
                          .filter_by(relationship=RelationShip.FOCUS)
                          .count() > 0)
    return (is_my_friend and is_his_friend)


def save_relationship(relationship):
    if not isinstance(relationship, RelationShip):
        return False
    else:
        session.add(relationship)
        session.commit()
        return True


def remove_relationship(relationship):
    if not isinstance(relationship, RelationShip):
        return False
    else:
        session.delete(relationship)
        session.commit()
        return True


def get_relationship(my_id, other_id, relation):
    if not my_id or not other_id or not relation:
        return None
    else:
        this_query = (query.filter_by(fromid=my_id).filter_by(toid=other_id)
                           .filter_by(relationship=relation))
        if this_query.count() > 0:
            return this_query.first()
        else:
            return None