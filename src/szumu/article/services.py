#!/usr/bin/env python
#-*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from szumu.article.model import Article


session = Session()
query = session.query(Article)


def save(article):
    if article is None or not isinstance(article, Article):
        return False
    else:
        session.add(article)
        session.commit()
        return True


def remove(article):
    if article is None or not isinstance(article, Article):
        return False
    else:
        session.delete(article)
        session.commit()
        return True


def find(id):
    if id is None or not isinstance(id, int):
        return None
    else:
        query_article = query.filter_by(id=id)
        if query_article.count() > 0:
            return query_article.first()
        else:
            return None


def find_by_author(author_id):
    if author_id is None or not isinstance(author_id, int):
        return None
    else:
        query_article = query.filter_by(author=author_id)
        if query_article.count() > 0:
            return query_article.all()
        else:
            return None


def find_by_shopid(shopid):
    if shopid is None or not isinstance(shopid, int):
        return None
    else:
        query_article = qurey.filter_by(shopid=shopid)
        if query_article.count() > 0:
            return query_article.all()
        else:
            return None