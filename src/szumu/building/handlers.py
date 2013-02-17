#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

from szumu.base import route
from szumu.web import json_encode, Controller
from szumu.user.model import User
from szumu.user import services as user_services
from szumu.building import special
from szumu.building import services as building_services
from szumu.course.model import Comment
from szumu.course import services as course_services
from szumu.article.model import Article
from szumu.article import services as article_services
from szumu.config import buildings as build_config


@route(r"/office/student/reg")
class Office(Controller):
    @tornado.web.authenticated
    def get(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self):
        message = []
        current_user = self.current_user
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

        if user_services.is_truename_existed(truename, current_user.username):
            success = False
            message.append('姓名已存在，若您未曾登记过信息，请联系站长')

        if user_services.is_number_existed(number, current_user.username):
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
            current_user.truename = truename
            current_user.birthday = birthday
            current_user.number = number
            current_user.college = college
            current_user.phone = phone
            current_user.shortPhone = short
            current_user.qq = qq
            current_user.state = 3
            user_services.update_user(current_user)

        self.finish({'success': success, 'message': message})


class BuildingHandler(Controller):
    def get_infor(self, special):
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
        self.get_infor(special.office)
        user = self.current_user
        self.render('buildings/office.html',
                    title=self.title, descr=self.descr, user=user)

    def post(self):
        raise tornado.web.HTTPError(405)


@route(r"/teach")
class Teach(BuildingHandler):
    @tornado.web.authenticated
    def get(self):
        self.check_whether_finish_truename_and_number()
        user = self.current_user
        truename = user.truename
        number = user.number
        courses = (course_services.get_stu_select_by_name_and_number(truename,
                                                                     number))
        classes = []
        if not courses is None:
            for course in courses:
                classes.append(course_services.find(course.cid))

        self.render('buildings/teach.html',
                    user=user, course=courses, classes=classes,
                    college_no=special.teach.college_no)

    def post(self):
        raise tornado.web.HTTPError(405)


@route(r"/teach/mate/classid/([0-9]+)")
class ClassMate(Controller):
    @tornado.web.authenticated
    def get(self, classid):
        self.check_whether_finish_truename_and_number()
        user = self.current_user
        username = user.username
        classes = course_services.find(classid)
        classinfor = []
        if classes is None:
            self.finish(json_encode({}))
        for one in classes:
            name = one.truename
            number = one.number
            checked_name = user_services.is_truename_existed(name,
                                                             username)
            checked_number = user_services.is_number_existed(number,
                                                             username)
            if (checked_name and checked_number):
                mate = user_services.get_user_by_name_and_number(name, number)
                picurl = md5("AvatarUrl:"+str(mate.id)).hexdigest()
                file_path = '/static/upfiles/avatar/' + picurl + '.png'
                if not os.path.isfile(file_path):
                    if mate['gender'] == 1:
                        picurl = 'male_big'
                    else:
                        picurl = 'female_big'
                classinfor.append({'id': mate.id,
                                   'nickname': mate.nickname,
                                   'pic': picurl})

        self.finish(json_encode(classinfor))

    def post(self):
        raise tornado.web.HTTPError(405)


@route(r"/teach/comment/classid/([0-9]+)")
class GetClassComment(Controller):
    @tornado.web.authenticated
    def get(self, classid):
        self.check_whether_finish_truename_and_number()

        user = self.current_user

        username = user.username
        comments = course_services.find_by_classid(classid)

        if not comments is None:
            for comment in comments:
                u = user_services.find(comment.userid)
                comment.nickname = u.nickname

        self.finish(json_encode(comments))

    @tornado.web.authenticated
    def post(self, classid):
        raise tornado.web.HTTPError(405)


@route(r"/teach/comment/new")
class NewClassComment(Controller):
    @tornado.web.authenticated
    def get(self, classid):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self):
        self.check_whether_finish_truename_and_number()

        classid = self.get_argument('classid', None)
        content = self.get_argument('comment', None)

        user = self.current_user

        success = True
        messages = []

        if not classid:
            success = False
            messages.append('获取课程信息出错')

        if not content:
            success = False
            messages.append('评论不能为空')

        if success:
            comment = Comment(classid, user.id, content)
            course_services.save_comment(comment)

        self.finish(json_encode({'success': success, 'messages': messages}))


@route(r"/tech")
class Tech(BuildingHandler):
    def get(self):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


class StudentHandler(BuildingHandler):
    def get(self):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


class StoneHandler(BuildingHandler):
    def get(self):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


class NorthHandler(BuildingHandler):
    def get(self):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


class SouthHandler(BuildingHandler):
    def get(self):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


class GymHandler(BuildingHandler):
    def get(self):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


class LiteraHandler(BuildingHandler):
    def get(self):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


class DormHandler(BuildingHandler):
    def get(self, id):
        pass

    def post(self):
        raise tornado.web.HTTPError(405)


@route(r"/rent/([0-9]+)")
class Rent(BuildingHandler):
    @tornado.web.authenticated
    def get(self, id):
        self.check_whether_finish_truename_and_number()
        if not id:
            raise tornado.web.HTTPError(405)
        house = building_services.find(id)
        self.render('buildings/rent.html', house=house,
                    rentType=build_config.RENT_TYPE)

    @tornado.web.authenticated
    def post(self, shop_id):
        self.check_whether_finish_truename_and_number()
        user = self.current_user
        user_id = user.id
        user_shop = building_services.get_shop_by_user(user_id)
        if user_shop:
            self.finish(json_encode({'success': False,
                                     'messages': ["您只能申请一次店铺。"]}))
        else:
            shop_name = self.get_argument('shopName', None)
            shop_type = self.get_argument('type', None)
            shop_descr = self.get_argument('descr', None)
            success = True
            messages = []

            if not shop_id:
                messages.append('该店铺不能申请')

            if not shopname:
                messages.append('请输入店铺名称')

            if not shoptype:
                messages.append('请选择店铺类型')

            if not shop_descr:
                messages.append('请输入店铺介绍')

            if not building_services.find_special(shop_id, 'rent'):
                messages.append('该店铺不能申请')

            if messages:
                success = False

            if success:
                shop = building_services.find(shop_id)
                shop.title = shop_name
                shop.ownerid = user_id
                shop.descr = shop_descr
                shop.special = shop_type
                building_services.save_building(shop)

            self.finish(json_encode({'success': success,
                                     'messages': messages}))


@route(r"/shop/(private|topic|sell)/([0-9]+)")
class Shop(BuildingHandler):
    @tornado.web.authenticated
    def get(self, type, id):
        user = self.current_user
        if (type == 'private'):
            shop = building_services.find(id)
            if not shop:
                raise tornado.web.HTTPError(404, '该店铺不存在')
            articles = article_services.find_by_shopid(id)
            self.render("buildings/shop/private.html",
                        user=user, shop=shop, articles=articles)
        if (type == 'sell'):
            shop = building_services.find(id)
            self.render("buildings/shop/sell.html", user=user, shop=shop)

    @tornado.web.authenticated
    def post(self, id):
        raise tornado.web.HTTPError(404)


@route(r"/shop/edit")
class EditShop(BuildingHandler):
    @tornado.web.authenticated
    def get(self):
        raise tornado.web.HTTPError(404)

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        shopid = self.get_argument('shopid', None)
        title = self.get_argument('shopName', None)
        descr = self.get_argument('descr', None)

        success = True
        messages = []

        if not shopid:
            success = False
            messages.append('该店铺不存在')

        shop = building_services.find(shopid)

        if not shop:
            success = False
            messages.append('该店铺不存在')
        else:
            if not shop.ownerid == user.id:
                success = False
                messages.append('您无权进行该操作')

        if not title:
            success = False
            messages.append('店铺名称不能为空')

        if not descr:
            success = False
            messages.append('店铺介绍不能为空')

        if success:
            editshop = building_services.find(shopid)
            editshop.title = title
            editshop.descr = descr
            building_services.update_building(editshop)

        self.finish(json_encode({'success': success, 'messages': messages}))


@route(r"/shop/private/article/new/([0-9]+)")
class NewPrivateArticle(BuildingHandler):
    @tornado.web.authenticated
    def get(self, id):
        raise tornado.web.HTTPError(404)

    @tornado.web.authenticated
    def post(self, id):
        shop = building_services.find(id)
        user = self.current_user
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        success = True
        messages = []

        if shop.ownerid != user.id:
            success = False
            messages.append('您无权进行该操作')

        if not title:
            success = False
            messages.append('标题不能为空')

        if not content:
            success = False
            messages.append('内容不能为空')

        if success:
            article = Article(title)
            article.content = content
            article.special = 'shop/private'
            article.shopid = id
            article.author = user.id
            article_services.save_article(article)

        self.finish(json_encode({'success': success, 'messages': messages}))


@route(r"/shop/private/article/del")
class DelPrivateArticle(BuildingHandler):
    @tornado.web.authenticated
    def get(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        shopid = self.get_argument('shopid')
        articleid = self.get_argument('articleid')

        success = True
        messages = []

        if not shopid:
            success = False
            messages.append('该店铺不存在')

        shop = building_services.find(shopid)

        if not shop:
            success = False
            messages.append('该店铺不存在')
        else:
            if not shop.ownerid == user.id:
                success = False
                messages.append('您无权进行该操作')

        if not articleid:
            success = False
            messages.append('找不到指定的文章')

        article = article_services.find(articleid)

        if not articleid:
            success = False
            messages.append('找不到指定的文章')

        if not article.author == user.id:
            success = False
            messages.append('您无权进行该操作')

        if not str(article.shopid) == shopid:
            success = False
            messages.append('您无权进行该操作')

        if success:
            article_services.remove_article(article)

        self.finish(json_encode({'success': success, 'messages': messages}))
