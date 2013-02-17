#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado

import szumu.chat.handlers
from szumu.base import route
from szumu.web import Controller
from szumu.map.model import Map
from szumu.map import services as map_services
from szumu.building import services as build_services
from szumu.building.special import special_map
from szumu.config import buildings as build_config


chat = szumu.chat.handlers.msgsrv


@route(r"/map/([0-9]+)")
class MapHandler(Controller):

    def get(self, mapid):
        map = map_services.find(int(mapid))
        if map is None:
            raise tornado.web.HTTPError(404, "Location Not Found")

        link = map.link.split(',')
        path = map.path.split(',')
        buildings_in_map = map.buildings.split(',')

        buildings = {}
        i = 0

        for building in buildings_in_map:
            if not building or building == 'None':
                buildings[i] = None
            elif building in special_map:
                buildings[i] = special_map[building].tostring()
            else:
                b = build_services.find(building)
                if b:
                    buildings[i] = b.tostring()
            i = i + 1

        self.set_cookie('lastview', mapid)

        special = [x['id'] for x in build_config.RENT_TYPE]
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
