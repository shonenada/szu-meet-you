#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

from szumu.web import json_encode, Controller
from szumu.user.model import User
from szumu.user import services as user_services
from szumu.message.model import Message
from szumu.message import services as msg_services
from szumu.base import route


@route("/user/msg/check")
class CheckMsg(Controller):

    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        userid = user.id
        have_new_msg = msg_services.check_new_msg(userid)
        if have_new_msg:
            msgs = msg_services.get_ones_receive_msg(userid)
            if len(msgs) < 10:
                self.finish(json_encode({'new_msg': True, 'num': len(msgs)}))
            else:
                self.finish(json_encode({'new_msg': True, 'num': 'N'}))
        else:
            self.finish(json_encode({'new_msg': False}))

    @tornado.web.authenticated
    def post(self):
        raise tornado.web.HTTPError(405)


@route(r"/user/msg/get/(send|receive)/")
class GetMsg(Controller):

    @tornado.web.authenticated
    def get(self, type):
        pageid = self.get_argument('page', 1)
        user = self.get_current_user()
        userid = user.id
        if (type == 'send'):
            msgs = msg_services.get_ones_send_msg(userid)
            if msgs:
                for msg in msgs:
                    man = user_services.find(msg.toid)
                    msg.man = man.nickname
        if (type == 'receive'):
            msgs = msg_services.get_ones_receive_msg(userid)
            if msgs:
                for msg in msgs:
                    man = user_services.find(msg.fromid)
                    msg.man = man.nickname

        msg_services.set_all_readed(userid)

        self.finish(json_encode(msgs))

    @tornado.web.authenticated
    def post(self, type):
        raise tornado.web.HTTPError(405)


@route(r"/user/msg/del/(send|receive)")
class DelMsg(Controller):

    @tornado.web.authenticated
    def get(self, kind):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self, kind):
        del_ids = self.get_arguments('delid', None)
        if not del_ids:
            self.finish(json_encode({'success': False,
                                     'message': '您未选择需删除的私信'}))

        user = self.get_current_user()
        userid = user.id

        if kind == 'send':
            for id in del_ids:
                msg = msg_services.find(id)
                if msg.fromid == user.id:
                    msg.hide_by_from()

        if kind == 'receive':
            for id in del_ids:
                msg = msg_services.find(id)
                if msg.toid == userid:
                    msg.hide_by_to()

        self.finish(json_encode({'success': True,
                                 'delID': del_ids}))


@route(r"/user/msg/send")
class SendMsg(Controller):
    @tornado.web.authenticated
    def get(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self):
        toid = self.get_argument('msg_id', None)
        if not toid:
            self.finish(json_encode({'success': False,
                                     'message': '您未选择私信对象'}))

        content = self.get_argument('send_content', None)
        if not content:
            self.finish(json_encode({'success': False,
                                     'message': '请输入回复的内容'}))

        user = self.get_current_user()
        user = user.as_array()
        userid = user['id']
        sendmsg = model.Message(userid, toid, content)
        sendmsg.save()
        self.finish(json_encode({'success': True}))


@route(r"/user/msg/re")
class ReMsg(Controller):
    @tornado.web.authenticated
    def get(self):
        raise tornado.web.HTTPError(405)

    @tornado.web.authenticated
    def post(self):
        msg_id = self.get_argument('msg_id', None)
        if not msg_id:
            self.finish(json_encode({'success': False,
                                     'message': '您未选择需回复的私信'}))

        content = self.get_argument('re_content', None)
        if not content:
            self.finish(json_encode({'success': False,
                                     'message': '请输入回复的内容'}))

        to_msg = msg_services.find(msg_id)
        if not to_msg:
            self.finish(json_encode({'success': False,
                                     'message': '您所回复的私信不存在'}))

        toid = to_msg.fromid
        user = self.get_current_user()
        userid = user.id
        remsg = Message(userid, toid, content)
        msg_services.save_msg(remsg)
        self.finish(json_encode({'success': True}))
