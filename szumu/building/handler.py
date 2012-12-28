#!/usr/bin/env python
#-*- coding: utf-8 -*-

from web import *

from szumu.building import special
from config.buildingConfig import buildingConfig
from szumu.articles.model import Aritcles
from szumu.building.shop import model as ShopModel
from szumu.users.model import User as UserModel

from hashlib import md5
import os

import szumu.chat
chat =  szumu.chat.handler.msgsrv


class BuildingHandler(Controller):
    
    def get_infor(self, special):
        special = special()
        self.title = special.title
        self.ownerid = special.ownerid
        self.pic = special.pic
        self.mapid = special.mapid
        self.mapsite = special.mapsite
        self.descr = special.descr
        self.color = special.color

        

class OfficeHandler(BuildingHandler):
    
    def get(self):
        self.get_infor(special.Office)
        user = self.get_current_user()
        if user:
            user = user.as_array()
        self.render('buildings/office.html',
                    title=self.title, 
                    descr=self.descr,
                    user=user,
                    )
            
    def post(self):
        raise httperror(404, 'Not Found')
    


class TeachHandler(BuildingHandler):
    
    @auth
    def get(self):
        self.check_whether_finish_truename_and_number()
        user = self.get_current_user()
        user = user.as_array()
        truename = user['truename']
        number = user['number']
        course = special.TeachingBuilding.get_class_infor_by_truename_and_number(self.db, truename, number)
        classes = []
        for x in course:
            classes.append(special.TeachingBuilding.get_course_infor_by_classid(self.db, x['cid']))
        self.render('buildings/teach.html', user=user, course=course, classes=classes, college_no=special.TeachingBuilding.college_no )
    
    def post(self):
        raise httperror(404, 'Not Found')

class ClassMateHandler(Controller):
    
    @auth
    def get(self, classid):
        self.check_whether_finish_truename_and_number()
        user = self.get_current_user()
        username = user.username
        classes = special.TeachingBuilding.get_class_infor_by_classid(self.db, classid)
        classinfor = []
        for x in classes:
            if UserModel.check_truename(self.db, 
                                        x['truename'], 
                                        username) and UserModel.check_number(self.db, 
                                                                             x['number'], 
                                                                             username):
                mate = UserModel.get_user_by_truename_and_number(self.db, x['truename'], x['number'])
                picurl = md5("AvatarUrl:"+str(mate['id'])).hexdigest()
                if not os.path.isfile('/static/upfiles/avatar/' + picurl + '.png'):
                    if mate['gender'] == 1:
                        picurl = 'male_big'
                    else:
                        picurl = 'female_big'
                classinfor.append({
                                   'id':mate['id'],
                                   'nickname':mate['nickname'],
                                   'pic':picurl,
                                   })
        self.finish(json_encode(classinfor))

    def post(self):
        raise httperror(404, 'Not Found')


class ClassCommentGetHandler(Controller):

    @auth
    def get(self, classid):
        self.check_whether_finish_truename_and_number()
        user = self.get_current_user()
        username = user.username
        comment = special.ClassComment.get_comment_by_classid(self.db, classid)
        for x in comment:
            u = UserModel.get_user_by_id(self.db, x['userid'])
            x['nickname'] = u['nickname']
        self.finish(json_encode(comment))

    @auth
    def post(self, classid):
        raise httperror(404, 'Not Found')
    
class ClassCommentNewHandler(Controller):

    @auth
    def get(self, classid):
        raise httperror(404, 'Not Found')

    @auth
    def post(self):
        self.check_whether_finish_truename_and_number()
        classid = self.get_argument('classid', None)
        content = self.get_argument('comment', None)
        user = self.get_current_user()
        user = user.as_array()
        
        success = True
        messages = []
        
        if not classid:
            success = False
            messages.append('获取课程信息出错')

        if not content:
            success = False
            messages.append('评论不能为空')
        
        if success:
            comment = special.ClassComment(classid, user['id'], content)
            comment.save()

        self.finish(json_encode({'success':success, 'messages':messages}))

class TechHandler(BuildingHandler):
    
    def get(self):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')



class StudentHandler(BuildingHandler):
    
    def get(self):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')



class StoneHandler(BuildingHandler):
   
    def get(self):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')


class NorthHandler(BuildingHandler):
    
    def get(self):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')



class SouthHandler(BuildingHandler):
    
    def get(self):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')


class GymHandler(BuildingHandler):
    
    def get(self):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')


class LiteraHandler(BuildingHandler):
    def get(self):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')


class DormHandler(BuildingHandler):
    def get(self, id):
        pass
    
    def post(self):
        raise httperror(404, 'Not Found')

class RentHandler(BuildingHandler):
    
    @auth
    def get(self, id):
        self.check_whether_finish_truename_and_number()
        if not id:
            raise httperror(404, 'Not Found')
        house = special.BeingRent.find(self.db, id)
        self.render('buildings/rent.html', house=house, rentType=buildingConfig.szumu_building_rent_type)

    @auth
    def post(self, id):
        self.check_whether_finish_truename_and_number()
        
        user = self.get_current_user().as_array()
        userid = user['id']

        user_shop = ShopModel.Shop.getCurrentUserShop(self.db, userid)
        
        if user_shop:
            self.finish(json_encode({'success':False,'messages':["您只能申请一次店铺。"]}))
        else:

            shopid = id
            shopname = self.get_argument('shopName', None)
            shoptype = self.get_argument('type', None)
            shopdescr = self.get_argument('descr', None)

            success = True
            messages = []

            if not shopid:
                messages.append('该店铺不能申请')

            if not shopname:
                messages.append('请输入店铺名称')

            if not shoptype:
                messages.append('请选择店铺类型')

            if not shopdescr:
                messages.append('请输入店铺介绍')

            if not special.BeingRent.find(self.db, shopid):
                messages.append('该店铺不能申请')

            if messages:
                success = False

            if success:
                shop = special.BeingRent()
                shop.initDB(self.db)
                shop.createShop(shopid)
                shop.title = shopname
                shop.ownerid = userid
                shop.descr = shopdescr
                shop.special = shoptype
                shop.save()
    
            self.finish(json_encode({'success':success,'messages':messages}))

class ShopHandler(BuildingHandler):

    @auth
    def get(self, type, id):
        user = self.get_current_user().as_array()
        if ( type == 'private' ):
            shop = ShopModel.PrivateShop.find(self.db, id)
            if not shop:
                raise httperror(404, '该店铺不存在')
            articles = ShopModel.PrivateShop.getArticlesByShopid(self.db, id)
            self.render("buildings/shop/private.html" , user=user, shop=shop, articles=articles)
        
        if ( type == 'sell' ):
            shop = ShopModel.SellShop.find(self.db, id)
            self.render("buildings/shop/sell.html", user=user, shop=shop)
        
    @auth
    def post(self, id):
        raise httperror(404)

class ShopEditHandler(BuildingHandler):
    @auth
    def get(self):
        raise httperror(404)
    
    @auth
    def post(self):
        user = self.get_current_user().as_array()
        shopid = self.get_argument('shopid', None)
        title = self.get_argument('shopName', None)
        descr = self.get_argument('descr', None)
        
        success = True
        messages= []
        
        if not shopid:
            success = False
            messages.append('该店铺不存在')
        
        shop = ShopModel.Shop.find(self.db, shopid)
        
        if not shop:
            success = False
            messages.append('该店铺不存在')
        else:
            if not shop['ownerid'] == user['id']:
                success = False
                messages.append('您无权进行该操作')
        
        if not title:
            success = False
            messages.append('店铺名称不能为空')
        
        if not descr:
            success = False
            messages.append('店铺介绍不能为空')
        
        if success:
            editshop = ShopModel.Shop(title, user['id'])
            editshop.id = shopid
            editshop.descr = descr
            editshop.update()
            
        self.finish(json_encode({'success':success, 'messages':messages}))
         
    
class PrivateNewArticleHandler(BuildingHandler):
    @auth
    def get(self, id):
        raise httperror(404)
                
    @auth
    def post(self, id):
        shop = ShopModel.PrivateShop.find(self.db, id)
        user = self.get_current_user().as_array()
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)        
        
        success = True
        messages = []
        
        if shop['ownerid'] != user['id']:
            success = False
            messages.append('您无权进行该操作')
        
        if not title:
            success = False
            messages.append('标题不能为空')
            
        if not content:
            success = False
            messages.append('内容不能为空')
        
        if success:
            article = Aritcles(title)
            article.content = content
            article.special = 'shop/private'
            article.shopid = id
            article.author = user['id']
            article.save()
            
        self.finish(json_encode({'success':success, 'messages':messages}))
        
        
class PrivateDelArticleHandler(BuildingHandler):
    @auth
    def get(self):
        raise httperror(404)

    @auth
    def post(self):
        user = self.get_current_user().as_array()
        shopid = self.get_argument('shopid')
        articleid = self.get_argument('articleid')

        success = True
        messages = []

        if not shopid:
            success = False
            messages.append('该店铺不存在')

        shop = ShopModel.PrivateShop.find(self.db, shopid)

        if not shop:
            success = False
            messages.append('该店铺不存在')
        else:
            if not shop['ownerid'] == user['id']:
                print "shop.ownerid != user.id"
                success = False
                messages.append('您无权进行该操作')

        if not articleid:
            success = False
            messages.append('找不到指定的文章')
    
        article = Aritcles.find(self.db, articleid)

        if not articleid:
            success = False
            messages.append('找不到指定的文章')

        if not article['author'] == user['id']:
            success = False
            messages.append('您无权进行该操作')

        if not str(article['shopid']) == shopid:
            success = False
            messages.append('您无权进行该操作')

        if success:
            delarticle = Aritcles(article['title'])
            delarticle.id = articleid
            delarticle.remove()

        self.finish(json_encode({'success':success,'messages':messages}))

        
        
        
        
        
        
        
        
        
        
        
        
        
        