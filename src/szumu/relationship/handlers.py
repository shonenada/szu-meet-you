#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time

import tornado.web

from szumu.web import Controller
from szumu.base import route
from szumu.relationship.model import RelationShip
from szumu.relationship import services as relationship_services


@route(r"/user/relation/friend/new/([0-9]+)")
class NewRelationship(Controller):
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
        relation = RelationShip(userid, friendid, RelationShip.FOCUS)
        relationship_services.save_relationship(relation)
        self.finish(json_encode({'success': True}))


@route(r"/user/relation/friend/remove/([0-9]+)")
class RemoveRelationship(Controller):
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
        relation = relationship_services.get_relationship(user_id, friend_id,
                                                          RelationShip.FOCUS)
        if relation:
            remove_relationship(relation)
        self.finish(json_encode({'success': True}))
