#!/usr/bin/env python
#-*- coding: utf-8 -*-
#encoding=utf-8

from hashlib import md5

import tornado

from szumu.database import DbMaster
from szumu.config.webConfig import Config


db = DbMaster.db


class User():
    
    id = None
    uesrname = None
    password = None
    hashed_password = None
    nickname = None
    truename = None
    gender = None
    number = None
    college = None
    birthday = None
    phone = None
    shortPhone = None
    qq = None
    regTime = None
    regIP = None
    logTime = None
    logIP = None
    state = None # 1:注册完成  2:已注销学籍注册  3:注册学籍
    trash = None
    
    table = "szu_mu_user"
    
    salt = Config.getSalt()
    
    def __init__(self, username, password, nickname, gender, ip):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.gender = gender
        self.remoteip = ip

    def hash_password(self, input_password):
        """ change the password of the current user """
        self.hashed_password = self._hash_password(self.salt, input_password)

    def update_log_time(self, log_time):
        return DbMaster.db.execute("UPDATE szu_mu_user SET logTime = %s where username = %s", log_time, self.username)

    def update_token(self, token):
        return DbMaster.db.execute("UPDATE szu_mu_user SET token = %s where username = %s", token, self.username)

    def update_log_ip(self, ip):
        return DbMaster.db.execute("UPDATE szu_mu_user SET logIP = %s where username = %s", ip, self.username)

    def create(self):
        self.hash_password(self.password)
        return DbMaster.db.execute("INSERT INTO szu_mu_user (username, password, nickname, gender, regIP, token) VALUES(%s, %s, %s, %s, %s, %s)" ,
                           self.username, self.hashed_password, self.nickname, self.gender, self.remoteip, ' ')

    def as_array(self):
        return DbMaster.db.get("SELECT * FROM szu_mu_user WHERE username = %s and password = %s", self.username, self.password )

    def updateinfor(self):
        return DbMaster.db.execute("UPDATE szu_mu_user SET "
                               "nickname=%s, gender=%s, truename=%s," 
                               "number=%s, college=%s, phone=%s, "
                               "shortPhone=%s, qq=%s ,"
                               "birthday=%s "
                               "WHERE username = %s" ,
                               self.nickname, self.gender, self.truename,
                               self.number, self.college, self.phone,
                               self.shortPhone, self.qq, self.birthday,
                               self.username,
                               )
        
    def reg_the_identity(self):
        return DbMaster.db.execute("UPDATE szu_mu_user SET "
                               "truename=%s, birthday=%s, number=%s, "
                               "college=%s, phone=%s, shortPhone=%s, "
                               "qq=%s, state=%s "
                               "WHERE username = %s" ,
                               self.truename, self.birthday, self.number,
                               self.college, self.phone, self.shortPhone,
                               self.qq, self.state, self.username
                               )
    
    
    @staticmethod
    def check_username_exist(username):
        """Judge whether the username is existed in the database """
        if not username : return None
        user = DbMaster.db.get("SELECT * FROM szu_mu_user where username = %s ", username)
        if not user:
            return False;
        else:
            return True;
        
    @staticmethod
    def check_nickname_exist(nickname, username=None):
        """Judge whether the username is existed in the database """
        if not nickname : return None
        if not username:
            user = DbMaster.db.get("SELECT * FROM szu_mu_user where nickname = %s ", nickname)
        else:
            user = DbMaster.db.get("SELECT * FROM szu_mu_user where nickname = %s and username <> %s", nickname, username )
        if not user:
            return False;
        else:
            return True;
    
    @staticmethod
    def check_username_and_password(salt, username, password):
        if not username or not password:
            raise tornado.web.HTTPError(401, "Auth failed")
        user = DbMaster.db.get("SELECT * FROM szu_mu_user WHERE username = %s "
                           "and password = %s",
                            username, User._hash_password(salt, password))
        if not user:
            return None
        else:
            return user['id']
        
    @staticmethod
    def check_truename(truename, current_username):
        if not DbMaster.db: return False
        if not truename: return False
        user = DbMaster.db.get("SELECT * FROM szu_mu_user WHERE truename = %s AND "
                      "username <> %s",
                      truename, current_username)
        if not user:
            return False
        else :
            return True
        
    @staticmethod
    def check_number(number, current_username):
        if not DbMaster.db: return False
        if not number: return False
        user = DbMaster.db.get("SELECT * FROM `szu_mu_user` WHERE number = %s AND "
                      "username <> %s",
                      number, current_username
                      )
        if not user:
            return False
        else:
            return True

    @staticmethod
    def get_user_by_id(userid):
        return DbMaster.db.get("SELECT * FROM `szu_mu_user` WHERE "
                        "id = %s",
                        int(userid))

    
    @staticmethod
    def get_user_by_truename_and_number(truename, number):
        return DbMaster.db.get("SELECT * FROM `szu_mu_user` WHERE "
                      "truename=%s AND number=%s",
                      truename, int(number)) 
    
    @staticmethod 
    def _hash_password(salt, raw_password):
        """ hash the raw password and return it """
        hashed_password = md5("<%s|%s>" % (salt, raw_password))
        return hashed_password.hexdigest()
    
    @staticmethod
    def _make_token(salt, ip, auth_time):
        return md5("<%s,%s|%s>" %(salt, ip, auth_time)).hexdigest()


class RelationShip():

    """ Table name = szu_mu_relationship
        Columns:
            id 
            fromid
            toid
            relationship
            created
    """
 
    fromid = None
    toid = None
    relationship = None
    relationship_focus = 1
    relationship_ignore = 0
    create = None

    def __init__(self, fromid, toid, relationship):
        self.fromid = fromid
        self.toid = toid
        self.relationship = relationship

    def save(self):
        if not self.fromid:
            return None
        if not self.toid:
            return None
        return DbMaster.db.execute('INSERT INTO `szu_mu_relationship` ' 
                                '(fromid, toid, relationship) '
                                'VALUES(%s, %s, %s)', 
                                int(self.fromid), 
                                int(self.toid),
                                int(self.relationship)
                                )

    def update(self):
        if not self.fromid:
            return None
        if not self.toid:
            return None
        if not self.relationship:
            return None
        return DbMaster.db.execute('UPDATE `szu_mu_relationship` '
                               'SET '
                               'relationship=%s ',
                               int(self.relationship)
                               )

    def remove(self):
        if not self.fromid:
            return None
        if not self.toid:
            return None
        if not self.relationship:
            return None
        return DbMaster.db.execute('DELETE FROM `szu_mu_relationship` '
                               'WHERE `fromid` = %s AND `toid` = %s ', self.fromid, self.toid)

    ''' 获取关系列表 '''
    @staticmethod
    def get_relationship_list(userid, kind, relationship):
        if not DbMaster.db: return None
        if not userid: return None
        if not kind: return None
        if not relationship: return None
        sql = "SELECT * FROM `szu_mu_relationship` WHERE "
        if kind == 'fromid':
            sql = sql + "fromid = %s "
        if kind == 'toid':
            sql = sql + "toid = %s "
        sql = sql + " AND relationship = %s"
        return DbMaster.db.query(sql, userid, relationship)

    ''' 关注的对象 '''
    @staticmethod
    def get_focus_list(userid):
        return RelationShip.get_relationship_list(userid, 'fromid', RelationShip.relationship_focus)

    ''' 黑名单 '''
    @staticmethod
    def get_ignore_list(userid):
        return RelationShip.get_relationship_list(userid, 'fromid', RelationShip.relationship_ignore)

    ''' 被关注列表 '''
    @staticmethod
    def get_focused_list(userid):
        return RelationShip.get_relationship_list(userid, 'toid', RelationShip.relationship_focus)

    ''' 被拉黑列表 '''
    @staticmethod
    def get_ignored_list(userid):
        return RelationShip.get_relationship_list(userid, 'toid', RelationShip.relationship_ignore)

    ''' 相互关注 '''
    @staticmethod
    def get_friends_list(userid):
        focus = RelationShip.get_focus_list(userid)
        focused = RelationShip.get_focused_list(userid)
        focused_list = []
        friends = []
        for x in focused:
            focused_list.append(x['fromid'])
        for x in focus:
            if x['toid'] in focused_list:
                friends.append(x['toid'])
        return friends

    ''' 检测两个用户的关系 '''
    @staticmethod
    def check_friended(userid, friendid):
        relationship = DbMaster.db.get('SELECT * FROM `szu_mu_relationship` WHERE '
                              ' `fromid` = %s AND `toid` = %s ',userid, friendid)
        return (relationship!=None)


class Message():
    """
        Table name = 'szu_mu_msg'
        Columns:
            id
            fromid
            toid
            msg
            created
            state
    """
    id = None
    fromid = None
    toid = None
    msg = None
    created = None
    state = None
    msg_state_readed = 1
    msg_state_not_read = 0
    from_hide = None
    to_hide = None

    def __init__(self, fromid, toid, msg, state=None):
        self.fromid = fromid
        self.toid = toid
        self.msg = msg
        if not state:
            state = self.msg_state_not_read
        self.state = state

    def save(self):
        if not self.fromid: return None
        if not self.toid: return None
        if not self.msg: return None
        if not self.state: self.state = self.msg_state_not_read
        DbMaster.db.execute("INSERT INTO `szu_mu_msg` (fromid, "
                         "toid, msg, state) VALUES ("
                         "%s, %s, %s, %s) ",
                          self.fromid,
                          self.toid,
                          self.msg,
                          self.state
                         )

    ''' 删除当前记录 '''
    def remove(self):
        if not self.id:
            return None
        return DbMaster.db.execute("DELETE FROM `szu_mu_msg` WHERE id=%s", int(self.id))

    ''' 发信者软删除当前记录 '''
    def hide_by_from(self):
        if not self.id:
            return None
        return DbMaster.db.execute("UPDATE `szu_mu_msg` SET `from_hide`=1 WHERE id=%s", int(self.id))

    ''' 收信者软删除当前记录 '''
    def hide_by_to(self):
        if not self.id:
            return None
        return DbMaster.db.execute("UPDATE `szu_mu_msg` SET `to_hide`=1 WHERE id=%s", int(self.id))

    ''' 获取私信对象 '''
    @staticmethod
    def find_msgob_by_id(id):
        msg = DbMaster.db.get('SELECT * FROM `szu_mu_msg` WHERE id=%s', int(id))
        if not msg:
            return None
        else:
            Msg = Message(msg['fromid'], msg['toid'], msg['msg'], msg['state'])
            Msg.id = id
            return Msg

    ''' 检测是否有新私信 '''
    @staticmethod
    def check_ones_msg(userid):
        if not DbMaster.db:
            return Nonec
        if not userid:
            return None
        msg = DbMaster.db.query("SELECT * FROM `szu_mu_msg` WHERE "
                        "toid=%s AND state=%s AND to_hide=0 ",
                         userid,
                         Message.msg_state_not_read
                         )
        if not msg:
            return False
        else:
            return msg

    ''' 更新私信状态 '''
    @staticmethod
    def updateMsgState(userid):
        if not DbMaster.db:
            return None
        if not userid:
            return None
        result = DbMaster.db.execute("UPDATE `szu_mu_msg` SET state=%s WHERE toid=%s", 
                            int(Message.msg_state_readed), 
                            int(userid))
        return result

    ''' 获取私信列表 '''
    @staticmethod
    def get_ones_msg(userid, kind):
        if not DbMaster.db: 
            return None
        if not userid:
            return None
        if not kind:
            return None

        sql = "SELECT * FROM szu_mu_msg WHERE "
        if kind == 'send':
            sql = sql + "fromid = %s AND `from_hide`=0"
        if kind == 'receive':
            sql = sql + "toid = %s AND `to_hide`=0"
        sql = sql + " ORDER BY `created` DESC "
        msg = DbMaster.db.query(sql,int(userid))
        if not msg:
            return None
        else:
            return msg

    ''' 获取私信（收到）列表 '''
    @staticmethod
    def get_ones_receive_msg(userid):
        return Message.get_ones_msg(userid, 'receive')

    ''' 获取私信（发送）列表 '''
    @staticmethod
    def get_ones_send_msg(userid):
        return Message.get_ones_msg(userid, 'send')
