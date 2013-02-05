#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
from szumu.web import Controller
import tornado.web
from szumu.chat.model import Chat


msgsrv = Chat(1)
json_encoder = json.JSONEncoder()
json_encode = json_encoder.encode


class ChatPageHandler(Controller):
    """ Build the handler of Chat"""
    def get(self):
        """ Rewrite GET method. """
        self.render('chat/chat.html', msgs=reversed(msgsrv.messages))


class ChatMessageHandler(Controller):
    @tornado.web.asynchronous
    def get(self):
        @msgsrv.listen
        def observer(id, msg):
            update_msg = json_encode({'id':id,'msg':msg})
            try:
                self.finish(update_msg)
            except IOError:
                pass
            
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        if not user :
            raise httperror(403, 'Forbidden')
        name = unicode(user.nickname).strip()
        content = unicode(self.get_argument("content")).strip()
        msgsrv.add_message("%s: %s" % (name,content))
