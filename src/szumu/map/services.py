#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sqlalchemy.orm import Session

from szumu.map.model import Map


session = Session()
query = session.query(Map)


def find(id):
    if id is None or not isinstance(id, int):
        return None
    else:
        query_map = query.filter_by(id=id)
        if query_map.count() > 0:
            return query_map.first()
        else:
            return None
        return None
        