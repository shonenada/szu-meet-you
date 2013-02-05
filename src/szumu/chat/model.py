#!/usr/bin/env python
#-*- coding: utf-8 -*-

import uuid
from szumu.database import dbMaster

unique_id = lambda: str(uuid.uuid1())

class Chat(object):
    
    servers = {}
    
    def __init__(self, id=None):
        self.id = id if id else unique_id()
        self.observers = []
        self.messages = []
        self.__class__.servers[id] = self
        
    def listen(self, success_callback):
        self.observers.append(success_callback)
        return success_callback
    
    def add_message(self, message, id=None):
        if not id:
            id = unique_id()
        try:
            self.messages.append((id,message))
            [callback(id, message) for callback in self.observers]
        finally:
            self.observers = []


class Msg(dbMaster):
    """ Table name = szu_mu_msg
        Columns:
            id
            fromid
            toid
            msg
            create
            state
            """
         
    fromid = None
    toid = None
    msg = None
    create = None
    state = None
    state_have_read = 1
    state_not_read = 0
     
    def __init__(self, fromid, toid, msg, state):
        self.fromid = fromid
        self.toid = toid
        self.msg = msg
        self.state
         

    def save(self):
        if not self.fromid:
            return None
        if not self.toid:
            return None
        return self.db.execute("INSERT INTO `szu_mu_msg`("
                               "fromid, toid, msg, state) "
                               "VALUES (%s, %s, %s, %s) ",
                               self.fromid,
                               self.toid,
                               self.msg,
                               self.state                              
                               )
        