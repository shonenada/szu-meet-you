#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2012-8-21
@author: Lyd
'''

import szumu.web
from szumu.base import route
from szumu.building.shop.model import Shop


@route(r"/user/myshop")
class CurrentUserShop(szumu.web.Controller):
    def get(self):
        current_user = self.get_current_user()
        if not current_user:
            raise httperror(403)
        user_shop = Shop.getCurrentUserShop(current_user.id)
        if not user_shop:
            self.write("您未申请店铺")
        else:
            self.redirect('/' + str(user_shop.special) + '/' +
                          str(user_shop.id))
