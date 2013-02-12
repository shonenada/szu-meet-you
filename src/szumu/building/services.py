from sqlalchemy.orm import Session

from szumu.building.base import BaseBuilding


session = Session()
query = session.query(BaseBuilding)


def find(id):
    if id is None or not isinstance(id, int):
        return None
    else:
        query_building = query.filter_by(id=id)
        if query_building.count() > 0:
            return query_building.first()
        else:
            return None
        return None


def find_special(id, special):
    if id is None or not isinstance(id, int):
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


def save(building):
    if building is None or not isinstance(building, BaseBuilding):
        return False
    else:
        session.add(building)
        session.commit()
        return True
