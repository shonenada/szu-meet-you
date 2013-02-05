#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

import szumu.web
from szumu.users import model
from szumu.base import route


@route("/account/msg/check")
class CheckMsg(szumu.web.Controller):
    @tornado.web.authenticated
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

    @tornado.web.authenticated
    def post(self):
        raise httperror(404, 'Not Found')


@route(r"/account/msg/get/(send|receive)/")
class GetMsg(szumu.web.Controller):
    @tornado.web.authenticated
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

    @tornado.web.authenticated
    def post(self, type):
        raise httperror(404, 'Not Found')


@route(r"/account/msg/del/(send|receive)")
class DelMsg(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self, kind):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
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


@route(r"/account/msg/send")
class SendMsg(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
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


@route(r"/account/msg/re")
class ReMsg(szumu.web.Controller):
    @tornado.web.authenticated
    def get(self):
        raise httperror(404, 'Not Found')

    @tornado.web.authenticated
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
        