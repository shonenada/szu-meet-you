#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json

import tornado.web

from szumu.base import route
from szumu.web import json_encode
from szumu.web import Controller
from szumu.chat.model import Chat


msgsrv = Chat(1)


@route(r"/chat")
class ChatPage(Controller):
    """ Build the handler of Chat"""
    def get(self):
        """ Rewrite GET method. """
        self.render('chat/chat.html', msgs=reversed(msgsrv.messages))


@route(r"/chat/messages")
class ChatMessage(Controller):
    @tornado.web.asynchronous
    def get(self):
        @msgsrv.listen
        def observer(id, msg):
            update_msg = json_encode({'id': id, 'msg': msg})
            try:
                self.finish(update_msg)
            except IOError:
                pass

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        if not user:
            raise httperror(403, 'Forbidden')
        name = user.nickname
        content = self.get_argument("content").strip()
        msgsrv.add_message("%s: %s" % (name, content))
