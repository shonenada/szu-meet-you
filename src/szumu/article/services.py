#!/usr/bin/env python
#-*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from szumu.article.model import Article


session = Session()
query = session.query(Article)


def save_article(article):
    if article is None or not isinstance(article, Article):
        return False
    else:
        session.add(article)
        session.commit()
        return True


def remove_article(article):
    if article is None or not isinstance(article, Article):
        return False
    else:
        session.delete(article)
        session.commit()
        return True


def find(id):
    if id is None:
        return None
    else:
        query_article = query.filter_by(id=id)
        if query_article.count() > 0:
            return query_article.first()
        else:
            return None


def find_by_author(author_id):
    if author_id is None:
        return None
    else:
        query_article = query.filter_by(author=author_id)
        if query_article.count() > 0:
            return query_article.all()
        else:
            return None


def find_by_shopid(shopid):
    if shopid is None:
        return None
    else:
        query_article = query.filter_by(shopid=shopid)
        if query_article.count() > 0:
            return query_article.all()
        else:
            return None