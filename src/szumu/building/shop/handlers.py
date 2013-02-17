#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-21
@author: Lyd
'''
import tornado.web

from szumu.web import Controller
from szumu.base import route
from szumu.building import services as building_services


@route(r"/user/myshop")
class CurrentUserShop(Controller):
    def get(self):
        current_user = self.current_user
        if not current_user:
            raise tornado.web.HTTPError(403)
        user_shop = building_services.get_shop_by_user(current_user.id)
        if not user_shop:
            self.write("您未申请店铺")
        else:
            self.redirect('/' + str(user_shop.special) + '/' +
                          str(user_shop.id))
