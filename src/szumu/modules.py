#/usr/bin/env python

from szumu.master.handlers import Home, AboutUs, ContactUs
from szumu.users.handlers import (UserSignUp, UserLogout, UserLogin, MyHome,
                                  Profile, UserInfor)
from szumu.building.handlers import Office
from szumu.relationship.handlers import NewRelationship, RemoveRelationship
from szumu.msg.handlers import CheckMsg, GetMsg, DelMsg, SendMsg
from szumu.map.handlers import Map, ViewLastMap


modules_master = [Home, AboutUs, ContactUs]
modules_users = [UserSignUp, UserLogout, UserLogin, MyHome, UserInfor]
modules_building = [Office]
modules_relationship = [NewRelationship, RemoveRelationship]
modules_msg = [CheckMsg, DelMsg, GetMsg, SendMsg]
modules_map = [Map, ViewLastMap]


modules = (modules_master + modules_users + modules_building +
           modules_relationship + modules_msg + modules_map)
