#!/usr/bin/env python
#-*- coding: utf-8 -*-

from web import *

from szumu.users import model
from config.webConfig import Config

import time

class UserSignUpHandler(Controller):
    def get(self):
        """ Rewrite the get method """
        self.check_whether_logged()
        self.render('auth/reg.html')
    
    def post(self):
        
        self.check_whether_logged()
        
        username = unicode(self.get_argument("username")).strip()
        password = unicode(self.get_argument("password")).strip()
        nickname = unicode(self.get_argument("nickname")).strip()
        gender = unicode(self.get_argument('gender', '1')).strip()
        
        message = []
        success = True
        
        if not username or len(username) <= 0 :
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
        
        if model.User.check_username_exist(self.db, username):
            success = False
            message.append('邮箱已存在，请更换后重新注册')
        
        if model.User.check_nickname_exist(self.db, nickname):
            success = False
            message.append('昵称已存在，请更换后重新注册')
        
        if success:
            ip = self.request.remote_ip
            user = model.User(username, password, nickname, gender, ip)
            userid = user.create()
            success = success and userid
            self.set_secure_cookie('userinfor', unicode(userid))
            self.set_secure_cookie('username', unicode(username))

        self.finish(json_encode({'success':success, 'message':message}))


class UserLoginHandler(Controller):

    def get(self):
        
        self.check_whether_logged()
        
        username = self.get_secure_cookie('username')
        if not username:
            username = 'example@example.com'
        self.render('auth/login.html', username=username)
    
    def post(self):
        
        self.check_whether_logged()
        
        username = unicode(self.get_argument("username")).strip()
        password = unicode(self.get_argument("password")).strip()
        
        message = []
        success = True
        
        if not username or len(username) <= 0 :
            message.append('邮箱不能用为')
            success = False
        
        if not password or len(password) <= 0:
            message.append('密码不能为空')
            success = False
        
        if len(password) < 6 or len(password) > 16 :
            message.append('密码长度应为6~16位')
            success = False
        
        userid = model.User.check_username_and_password(self.db, model.User.salt, username, password)
        
        if not userid:
            """ Log Failed """
            message.append('帐号或密码错误')
            success = False
            
        else:
            """ Log succeed """
            """ Update some information of the logged user """
            self.set_secure_cookie('userinfor', unicode(userid))
            self.set_secure_cookie('username', unicode(username))
            current_user = self.get_current_user(unicode(userid))
            remote_ip = self.request.remote_ip
            log_time = time.strftime('%Y-%m-%d %H:%I:%S',time.localtime(time.time()))
            token = model.User._make_token(Config.get_token_salt(), remote_ip, log_time)
            current_user.update_log_time(log_time)
            current_user.update_token(token)
            current_user.update_log_ip(remote_ip)
            self.set_secure_cookie('token', token)
            
        self.finish(json_encode({'success': success, 'message':message}))
            
        
                           
class UserLogOutHandler(Controller):
    
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')
                
    def post(self):
        raise httperror(404, "Not Found")
    
    
    
class MyHomeHandler(Controller):
    
    @auth
    def get(self):
        self.redirect('/map/2')
        # self.render('account/myhome.html')
    
    @auth
    def post(self):
        pass
    
    
class ProfileHandler(Controller):
    @auth
    def get(self):
        current_user = self.get_current_user()
        if current_user :
            current_user = current_user.as_array()
        self.render('account/profile.html', user=current_user)
        
    @auth
    def post(self):
        message = []
        
        user = self.get_current_user()
                     
        nickname = self.get_argument('nickname', None)
        gender = self.get_argument('gender', None)
        truename = self.get_argument('truename', None)
        number = self.get_argument('number', 0)
        college = self.get_argument('college', 0)
        birthday = self.get_argument('birthday', 0000-00-00)
        phone = self.get_argument('phone', 0)
        short = self.get_argument('short', 0)
        qq = self.get_argument('qq', 0)
        
        success = True
        
        if not nickname:
            success = False
            message.append('昵称不能为空')
            
        if model.User.check_nickname_exist(self.db, nickname, self.get_current_user().username):
            success = False
            message.append('昵称已存在，请更换后重试')
            
        if model.User.check_truename(self.db, truename, user.username):
            success = False
            message.append('姓名已存在，若您未曾登记过信息，请联系站长')
            
        if model.User.check_number(self.db, number, user.username):
            success = False
            message.append('学号已存在，若您未曾登记过信息，请联系站长')
            
        if not gender:
            success = False
            message.append('性别不能为空')

        if success:
            current_user = self.get_current_user()
            current_user.nickname = nickname
            current_user.gender = gender
            current_user.truename = truename
            current_user.number = number
            current_user.college = college
            current_user.birthday = birthday
            current_user.phone = phone
            current_user.shortPhone = short
            current_user.qq = qq
            current_user.updateinfor()
            
        self.finish(json_encode({'success':success,'message':message}))
    
class UserInforGetHandler(Controller):
    @auth
    def get(self, userid):
        user = self.get_current_user().as_array()
        myid = user['id']        
        mate = model.User.get_user_by_id(self.db, userid)
        self.finish(json_encode({
                                 'id':mate['id'],
                                 'nickname':mate['nickname'],
                                 'college':mate['college'],
                                 'friended':model.RelationShip.check_friended(self.db, myid, mate['id']),
                                 }))
        
    @auth
    def post(self, userid):
        raise httperror(404)
    
class OfficeHandler(Controller):
    @auth
    def get(self):
        raise httperror(404, 'Not Found')
    
    @auth
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
    
        if model.User.check_truename(self.db, truename, user.username):
            success = False
            message.append('姓名已存在，若您未曾登记过信息，请联系站长')
            
        if model.User.check_number(self.db, number, user.username):
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
        
        self.finish({'success':success,'message':message})


class MsgCheckHandler(Controller):

    @auth
    def get(self):
        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        msg = model.Message.check_ones_msg(self.db, userid)
        if not msg:
            self.finish(json_encode({'newMsg':False}))
        else:
            if len(msg)<10:
                self.finish(json_encode({'newMsg':True,'num':len(msg)}))
            else:
                self.finish(json_encode({'newMsg':True,'num':'N'}))
            
    @auth
    def post(self):
        raise httperror(404, 'Not Found')


class MsgGetHandler(Controller):
    @auth
    def get(self, type):
        pageid = self.get_argument('page', 1)
        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        if (type == 'send'):
            msg = model.Message.get_ones_send_msg(self.db, userid)
            if msg:
                for x in msg:
                    man = model.User.get_user_by_id(self.db, x['toid'])
                    x['man'] = man['nickname']
        if (type == 'receive'):
            msg = model.Message.get_ones_receive_msg(self.db, userid)
            if msg:
                for x in msg:
                    man = model.User.get_user_by_id(self.db, x['fromid'])
                    x['man'] = man['nickname']

        model.Message.updateMsgState(self.db, userid)
        
        self.finish(json_encode(msg))

    @auth
    def post(self, type):
        raise httperror(404, 'Not Found')

class MsgDelHandler(Controller):
    @auth
    def get(self, kind):
        raise httperror(404, 'Not Found')

    @auth
    def post(self, kind):
        delid = self.get_arguments('delid', None)
        if not delid:
            self.finish(json_encode({'success':False,'message':'您未选择需删除的私信'}))

        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']

        if kind == 'send':
            for x in delid:
                msg = model.Message.find_msgob_by_id(self.db, x)
                if msg.fromid == user.id:
                    msg.hide_by_from()

        if kind == 'receive':
            for x in delid:
                msg = model.Message.find_msgob_by_id(self.db, x)
                if msg.toid == userid:
                    msg.hide_by_to()

        self.finish(json_encode({'success':True,'delID':delid}))

class MsgSendHandler(Controller):
    @auth
    def get(self):
        raise httperror(404, 'Not Found')

    @auth
    def post(self):
        toid = self.get_argument('msg_id', None)
        if not toid:
            self.finish(json_encode({'success':False,'message':'您未选择私信对象'}))

        content = self.get_argument('send_content', None)
        if not content:
            self.finish(json_encode({'success':False,'message':'请输入回复的内容'}));

        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        sendmsg = model.Message(userid, toid, content)
        sendmsg.save()
        self.finish(json_encode({'success':True}))


class MsgReHandler(Controller):
    @auth
    def get(self):
        raise httperror(404, 'Not Found')

    @auth
    def post(self):
        msgid = self.get_argument('msg_id', None)
        if not msgid:
            self.finish(json_encode({'success':False,'message':'您未选择需回复的私信'}))

        content = self.get_argument('re_content', None)
        if not content:
            self.finish(json_encode({'success':False,'message':'请输入回复的内容'}));

        tomsg = model.Message.find_msgob_by_id(self.db, msgid)
        if not tomsg:
            self.finish(json_encode({'success':False,'message':'您所回复的私信不存在'}));
        
        toid = tomsg.fromid
        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        remsg = model.Message(userid, toid, content)
        remsg.save()
        self.finish(json_encode({'success':True}))


class NewRelationshipHandler(Controller):
    @auth
    def get(self):
        raise httperror(404, 'Not Found')

    @auth
    def post(self):
        raise httperror(404, 'Not Found')

    @auth
    def put(self, friendid):
        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        relation = model.RelationShip(userid, friendid, model.RelationShip.relationship_focus)
        relation.save()
        self.finish(json_encode({'success':True}))


class RemoveRelationshipHandler(Controller):
    @auth
    def get(self):
        raise httperror(404, 'Not Found')

    @auth
    def post(self):
        raise httperror(404, 'Not Found')

    @auth
    def put(self, friendid):
        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        relation = model.RelationShip(userid, friendid, model.RelationShip.relationship_focus)
        relation.remove()
        self.finish(json_encode({'success':True}))