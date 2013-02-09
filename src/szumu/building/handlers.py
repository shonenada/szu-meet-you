#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

import szumu.web
from szumu.web import json_encode
from szumu.users import model
from szumu.base import route
from szumu.building import special
from szumu.building.shop import model as ShopModel


@route(r"/office/student/reg")
class Office(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
    def post(self):
        message = []
        user = self.get_current_user()
        truename = unicode(self.get_argument('truename', None)).strip()
        birthday = unicode(self.get_argument('birthday', '0000-00-00')).strip()
        number = unicode(self.get_argument('number', None)).strip()
        college = unicode(self.get_argument('college', 0)).strip()
        phone = unicode(self.get_argument('phone', 0)).strip()
        short = unicode(self.get_argument('short', 0)).strip()
        qq = unicode(self.get_argument('qq', 0)).strip()

        success = True

        if not truename:
            message.append('真实姓名不能为空')
            success = False

        if model.User.check_truename(truename, user.username):
            success = False
            message.append('姓名已存在，若您未曾登记过信息，请联系站长')

        if model.User.check_number(number, user.username):
            success = False
            message.append('学号已存在，若您未曾登记过信息，请联系站长')

        if birthday == '0000-00-00':
            message.append('生日不能为空')
            success = False

        if not number:
            message.append('学号不能为空')
            success = False

        if college == 0:
            message.append('学院不能为空')
            success = False

        if success:
            user.truename = truename
            user.birthday = birthday
            user.number = number
            user.college = college
            user.phone = phone
            user.shortPhone = short
            user.qq = qq
            user.state = 3
            user.reg_the_identity()

        self.finish({'success': success, 'message': message})


class BuildingHandler(szumu.web.Controller):
    def get_infor(self, special):
        special = special()
        self.title = special.title
        self.ownerid = special.ownerid
        self.pic = special.pic
        self.mapid = special.mapid
        self.mapsite = special.mapsite
        self.descr = special.descr
        self.color = special.color


@route("/office")
class OfficePage(BuildingHandler):
    def get(self):
        self.get_infor(special.Office)
        user = self.get_current_user()
        if user:
            user = user.as_array()
        self.render('buildings/office.html',
                    title=self.title, descr=self.descr, user=user)

    def post(self):
        raise httperror(404, 'Not Found')


@route(r"/teach")
class Teach(BuildingHandler):
    @tornado.web.authenticated
    def get(self):
        self.check_whether_finish_truename_and_number()
        user = self.get_current_user()
        user = user.as_array()
        truename = user['truename']
        number = user['number']
        course = (special.TeachingBuilding
                  .get_class_infor_by_truename_and_number(truename, number))
        classes = []
        for x in course:
            (classes.append(special.TeachingBuilding
             .get_course_infor_by_classid(x['cid'])))
        self.render('buildings/teach.html',
                    user=user, course=course, classes=classes,
                    college_no=special.TeachingBuilding.college_no)

    def post(self):
        raise httperror(404, 'Not Found')


@route(r"/teach/mate/classid/([0-9]+)")
class ClassMate(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self, classid):
        self.check_whether_finish_truename_and_number()
        user = self.get_current_user()
        username = user.username
        classes = special.TeachingBuilding.get_class_infor_by_classid(classid)
        classinfor = []
        for x in classes:
            if (UserModel.check_truename(x['truename'], username) and
                UserModel.check_number(x['number'], username)):
                mate = UserModel.get_user_by_truename_and_number(x['truename'],
                                                                 x['number'])
                picurl = md5("AvatarUrl:"+str(mate['id'])).hexdigest()
                file_path = '/static/upfiles/avatar/' + picurl + '.png'
                if not os.path.isfile(file_path):
                    if mate['gender'] == 1:
                        picurl = 'male_big'
                    else:
                        picurl = 'female_big'
                classinfor.append({'id': mate['id'],
                                   'nickname': mate['nickname'],
                                   'pic': picurl})
        self.finish(json_encode(classinfor))

    def post(self):
        raise httperror(404, 'Not Found')


@route(r"/teach/comment/classid/([0-9]+)")
class GetClassComment(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self, classid):
        self.check_whether_finish_truename_and_number()
        user = self.get_current_user()
        username = user.username
        comment = special.ClassComment.get_comment_by_classid(classid)
        for x in comment:
            u = UserModel.get_user_by_id(x['userid'])
            x['nickname'] = u['nickname']
        self.finish(json_encode(comment))

    @tornado.web.authenticated
    def post(self, classid):
        raise httperror(404, 'Not Found')


@route(r"/teach/comment/new")
class NewClassComment(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self, classid):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
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
        self.finish(json_encode({'success': success, 'messages': messages}))


@route(r"/tech")
class Tech(BuildingHandler):
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


@route(r"/rent/([0-9]+)")
class Rent(BuildingHandler):
    @tornado.web.authenticated
    def get(self, id):
        self.check_whether_finish_truename_and_number()
        if not id:
            raise httperror(404, 'Not Found')
        house = special.BeingRent.find(id)
        self.render('buildings/rent.html', house=house,
                    rentType=buildingConfig.szumu_building_rent_type)

    @tornado.web.authenticated
    def post(self, id):
        self.check_whether_finish_truename_and_number()
        user = self.get_current_user().as_array()
        userid = user['id']
        user_shop = ShopModel.Shop.getCurrentUserShop(userid)
        if user_shop:
            self.finish(json_encode({'success': False,
                                     'messages': ["您只能申请一次店铺。"]}))
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

            if not special.BeingRent.find(shopid):
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

            self.finish(json_encode({'success': success,
                                     'messages': messages}))


@route(r"/shop/(private|topic|sell)/([0-9]+)")
class Shop(BuildingHandler):
    @tornado.web.authenticated
    def get(self, type, id):
        user = self.get_current_user().as_array()
        if (type == 'private'):
            shop = ShopModel.PrivateShop.find(id)
            if not shop:
                raise httperror(404, '该店铺不存在')
            articles = ShopModel.PrivateShop.getArticlesByShopid(id)
            self.render("buildings/shop/private.html",
                        user=user, shop=shop, articles=articles)
        if (type == 'sell'):
            shop = ShopModel.SellShop.find(id)
            self.render("buildings/shop/sell.html", user=user, shop=shop)

    @tornado.web.authenticated
    def post(self, id):
        raise httperror(404)


@route(r"/shop/edit")
class EditShop(BuildingHandler):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404)

    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user().as_array()
        shopid = self.get_argument('shopid', None)
        title = self.get_argument('shopName', None)
        descr = self.get_argument('descr', None)

        success = True
        messages = []

        if not shopid:
            success = False
            messages.append('该店铺不存在')

        shop = ShopModel.Shop.find(shopid)

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

        self.finish(json_encode({'success': success, 'messages': messages}))


@route(r"/shop/private/article/new/([0-9]+)")
class NewPrivateArticle(BuildingHandler):
    @tornado.web.authenticated
    def get(self, id):
        raise httperror(404)

    @tornado.web.authenticated
    def post(self, id):
        shop = ShopModel.PrivateShop.find(id)
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

        self.finish(json_encode({'success': success, 'messages': messages}))


@route(r"/shop/private/article/del")
class DelPrivateArticle(BuildingHandler):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404)

    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user().as_array()
        shopid = self.get_argument('shopid')
        articleid = self.get_argument('articleid')

        success = True
        messages = []

        if not shopid:
            success = False
            messages.append('该店铺不存在')

        shop = ShopModel.PrivateShop.find(shopid)

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

        article = Aritcles.find(articleid)

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

        self.finish(json_encode({'success': success, 'messages': messages}))
