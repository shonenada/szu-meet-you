#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time

import tornado.web

from szumu.web import Controller
from szumu.web import json_encode
from szumu.base import route
from szumu.user.model import User
from szumu.relation.model import Relation
from szumu.user import services as user_services
from szumu.relation import services as relation_services


@route("/signup")
class SignUp(Controller):

    def get(self):
        self.check_whether_logged()
        self.render('signup.html', MALE_VALUE=User.GENDER_MALE,
                    FEMALE_VALUE=User.GENDER_FEMALE)

    def post(self):
        self.check_whether_logged()

        username = self.get_argument("username").strip()
        password = self.get_argument("password").strip()
        nickname = self.get_argument("nickname").strip()
        gender = self.get_argument('gender', '1').strip()

        message = []
        success = True

        if not username or len(username) <= 0:
            success = False
            message.append('邮箱不能为空')

        if not password or len(password) <= 0:
            success = False
            message.append('密码不能为空')

        if len(password) < 6 or len(password) > 16:
            success = False
            message.append('密码长度有误，密码长度为6~16位')

        if not nickname or len(nickname) <= 0:
            success = False
            message.append('昵称不能为空 ')

        if user_services.is_username_existed(username):
            success = False
            message.append('邮箱已存在，请更换后重新注册')

        if user_services.is_nickname_existed(nickname):
            success = False
            message.append('昵称已存在，请更换后重新注册')

        if success:
            ip = self.request.remote_ip
            user = User(username, password, nickname)
            user.gender = gender
            user.ip = ip
            user_services.save_user(user)

            userid = user_services.get_id_by_username(username)

            self.set_secure_cookie('userinfor', unicode(userid))
            self.set_secure_cookie('username', unicode(username))

        self.finish(json_encode({'success': success, 'message': message}))


@route("/signin")
class SignIn(Controller):
    def get(self):
        self.check_whether_logged()
        username = self.get_secure_cookie('username')
        if not username:
            username = 'example@example.com'
        self.render('signin.html', username=username)

    def post(self):
        self.check_whether_logged()
        username = self.get_argument("username").strip()
        password = self.get_argument("password").strip()
        message = []
        success = True

        if not username or len(username) <= 0:
            message.append('邮箱不能用为')
            success = False

        if not password or len(password) <= 0:
            message.append('密码不能为空')
            success = False

        if len(password) < 6 or len(password) > 16:
            message.append('密码长度应为6~16位')
            success = False

        is_pass_login = user_services.login_validate(username, password)

        if not is_pass_login:
            """ Log Failed """
            message.append('帐号或密码错误')
            success = False

        else:
            """ Log succeed """
            """ Update some information of the logged user """
            userid = user_services.get_id_by_username(username)

            self.set_secure_cookie('userinfor', unicode(userid))
            self.set_secure_cookie('username', unicode(username))

            current_user = user_services.find(userid)

            remote_ip = self.request.remote_ip
            log_time = time.strftime('%Y-%m-%d %H:%I:%S',
                                     time.localtime(time.time()))

            token_salt = self.application.config['token_salt']
            token = User._make_token(token_salt, remote_ip, log_time)

            current_user.update_log_infor(token, remote_ip, log_time)

            self.set_secure_cookie('token', token)

        self.finish(json_encode({'success': success, 'message': message}))


@route("/signout")
class SignOut(Controller):

    def get(self):
        self.clear_all_cookies()
        self.redirect('/')

    def post(self):
        raise tornado.web.HTTPError(405)


@route('/home')
class MyHome(Controller):

    @tornado.web.authenticated
    def get(self):
        self.redirect('/map/2')
        # self.render('user/myhome.html')

    @tornado.web.authenticated
    def post(self):
        pass


@route('/user/profile')
class Profile(Controller):
    @tornado.web.authenticated
    def get(self):
        current_user = self.current_user
        self.render('user/profile.html', user=current_user,
                    MALE_VALUE=User.GENDER_MALE,
                    FEMALE_VALUE=User.GENDER_FEMALE)

    @tornado.web.authenticated
    def post(self):
        message = []

        user = self.current_user

        nickname = self.get_argument('nickname', None)
        gender = self.get_argument('gender', None)
        truename = self.get_argument('truename', None)
        number = self.get_argument('number', 0)
        college = self.get_argument('college', 0)
        birthday = self.get_argument('birthday', 0000-00-00)
        qq = self.get_argument('qq', 0)

        success = True

        if not nickname:
            success = False
            message.append('昵称不能为空')

        if user_services.is_nickname_existed(nickname, user.username):
            success = False
            message.append('昵称已存在，请更换后重试')

        if user_services.is_truename_existed(truename, user.username):
            success = False
            message.append('姓名已存在，若您未曾登记过信息，请联系站长')

        if user_services.is_number_existed(number, user.username):
            success = False
            message.append('学号已存在，若您未曾登记过信息，请联系站长')

        if not gender:
            success = False
            message.append('性别不能为空')

        if success:
            current_user = self.current_user
            current_user.nickname = nickname
            current_user.gender = gender
            current_user.truename = truename
            current_user.number = number
            current_user.college = college
            current_user.birthday = birthday
            current_user.qq = qq
            user_services.update_user(current_user)

        self.finish(json_encode({'success': success, 'message': message}))


@route(r'/user/userinfor/get/([0-9]+)')
class UserInfor(Controller):
    @tornado.web.authenticated
    def get(self, user_id):
        current_user = self.current_user
        my_id = current_user.id
        mate = user_services.find(user_id)
        friended = relation_services.is_each_friend(my_id, mate.id)
        self.finish(json_encode({'id': mate.id,
                                 'nickname': mate.nickname,
                                 'college': mate.college,
                                 'friended': friended}))

    @tornado.web.authenticated
    def post(self, userid):
        raise tornado.web.HTTPError(405)


@route('/resident')
class Resident(Controller):
    @tornado.web.authenticated
    def get(self):
        page = self.get_argument('page', 1)

        current_user = self.current_user

        user_list = user_services.get_user_list(int(page))

        user_services.with_avatar(user_list)
        relation_services.with_relation(current_user.id, user_list)

        FOCUS_VALUE = Relation.FOCUS
        IGNORE_VALUE = Relation.IGNORE

        self.render('resident.html', user_list=user_list,
                    FOCUS_VALUE=FOCUS_VALUE, IGNORE_VALUE=IGNORE_VALUE)

    @tornado.web.authenticated
    def post(self):
        raise tornado.web.HTTPError(405)


@route('/user/friends')
class Friends(Controller):

    @tornado.web.authenticated
    def get(self):
        current_user = self.current_user
        user_id = current_user.id

        my_friends = relation_services.get_focus_list(user_id)
        my_ignored = relation_services.get_ignore_list(user_id)
        focus_me = relation_services.get_being_focused_list(user_id)
        
        user_services.with_avatar(my_friends)

        self.render('user/friends.html', myfriends=my_friends,
                    focusme=focus_me, myignored=my_ignored)

    def post(self):
        raise tornado.web.HTTPError(405)
