#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time

import tornado.web

import szumu.web
from szumu.users import model
from szumu.base import route


@route(r"/account/relation/friend/new/([0-9]+)")
class NewRelationship(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
    def post(self):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
    def put(self, friendid):
        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        relation = model.RelationShip(userid, friendid,
                                      model.RelationShip.relationship_focus)
        relation.save()
        self.finish(json_encode({'success': True}))


@route(r"/account/relation/friend/remove/([0-9]+)")
class RemoveRelationship(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
    def post(self):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
    def put(self, friendid):
        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        relation = model.RelationShip(userid, friendid,
                                      model.RelationShip.relationship_focus)
        relation.remove()
        self.finish(json_encode({'success': True}))
