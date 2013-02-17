from sqlalchemy.orm import Session

from szumu.building.base import BaseBuilding


session = Session()
query = session.query(BaseBuilding)


def find(id):
    if id is None:
        return None
    else:
        query_building = query.filter_by(id=id)
        if query_building.count() > 0:
            return query_building.first()
        else:
            return None
        return None


def find_special(id, special):
    if id is None:
        return None
    is_special = (special in ['rent', 'office', 'student', 'stone', 'tech',
                              'teach', 'litera', 'north', 'south', 'gym',
                              'sold', 'dorm', 'beingBuilt'])
    if is_special:
        query_building = query.filter_by(id=id).filter_by(special=special)
        if query_building.count() > 0:
            return query_building.first()
        else:
            return None
    else:
        return None


def save_building(building):
    if building is None or not isinstance(building, BaseBuilding):
        return False
    else:
        session.add(building)
        session.commit()
        return True


def update_building(building):
    if building is None or not isinstance(building, BaseBuilding):
        return False
    else:
        this_query = query.filter_by(id=building.id)
        if this_query.count() > 0:
            query_building = this_query.first()
            query_building.title = building.title
            query_building.descr = building.descr
            session.commit()
            return True


def get_shop_by_user(user_id):
    if user_id is None:
        return None
    else:
        this_query = query.filter_by(ownerid=user_id)
        if this_query.count() > 0:
            return this_query.first()
        else:
            return None
