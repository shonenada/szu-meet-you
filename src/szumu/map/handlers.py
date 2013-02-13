#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado

import szumu.chat.handlers
from szumu.base import route
from szumu.web import Controller
from szumu.map.model import Map
from szumu.map.services import find
from szumu.building.base import BaseBuilding
from szumu.building.special import *
from szumu.config import buildings as builds


chat = szumu.chat.handlers.msgsrv


@route(r"/map/([0-9]+)")
class MapHandler(Controller):

    def get(self, mapid):
        map = find(int(mapid))
        if map is None:
            raise tornado.web.HTTPError(405)

        link = map.link.split(',')
        path = map.path.split(',')
        build = map.buildings.split(',')

        buildings = {}
        i = 0

        for x in build:
            if not x or x == 'None':
                buildings[i] = None
            elif x in special_map:
                buildings[i] = special_map[x].tostring()
            else:
                buildings[i] = BaseBuilding.find(x)
            i = i + 1

        # current_user = self.get_current_user()
        # if not current_user is None:
        #     current_user = current_user.as_array()

        self.set_cookie('lastview', mapid)

        special = [x['id'] for x in builds.RENT_TYPE]
        special.append('rent')

        self.render('map.html', map=map.link, title=map.title,
                    descr=map.descr, link=link, path=path,
                    buildings=buildings, msgs=chat.messages, special=special)

    def post(self):
        raise tornado.web.HTTPError(405)


@route(r"/map")
class ViewLastMap(Controller):
    def get(self):
        lastview = unicode(self.get_cookie('lastview'))
        if lastview:
            self.redirect('/map/' + lastview)
        else:
            raise tornado.web.HTTPError(405)

    def post(self):
        raise tornado.web.HTTPError(405)
