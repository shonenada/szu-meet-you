#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time

import tornado.web

from szumu.web import Controller
from szumu.base import route
from szumu.relation.model import Relation
from szumu.relation import services as relation_services


@route(r"/user/relation/friend/new/([0-9]+)")
class NewRelation(Controller):
    @tornado.web.authenticated
    def get(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def put(self, friendid):
        user = self.current_user
        userid = user.id
        relation = Relation(userid, friendid, Relation.FOCUS)
        relation_services.save_relation(relation)
        self.finish(json_encode({'success': True}))


@route(r"/user/relation/friend/remove/([0-9]+)")
class RemoveRelation(Controller):
    @tornado.web.authenticated
    def get(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def put(self, friend_id):
        user = self.current_user
        user_id = user.id
        relation = relation_services.get_relation(user_id, friend_id)
        if relation:
            remove_relation(relation)
        self.finish(json_encode({'success': True}))
