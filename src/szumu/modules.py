#/usr/bin/env python
from szumu.master.handlers import Home, AboutUs, ContactUs
from szumu.user.handlers import (SignUp, SignOut, SignIn, MyHome,
                                 Profile, UserInfor, Resident, Friends)
from szumu.building.handlers import (Office, OfficePage, Teach, ClassMate,
                                     GetClassComment, NewClassComment, Tech,
                                     Rent, Shop, EditShop, NewPrivateArticle)
from szumu.relation.handlers import NewRelation, RemoveRelation
from szumu.message.handlers import CheckMsg, GetMsg, DelMsg, SendMsg
from szumu.map.handlers import MapHandler, ViewLastMap
from szumu.chat.handlers import ChatPage, ChatMessage
from szumu.building.shop.handlers import CurrentUserShop


modules_master = [Home, AboutUs, ContactUs]
modules_users = [SignUp, SignOut, SignIn, MyHome, UserInfor, Profile, Resident,
                 Friends]
modules_building = [Office, OfficePage, Teach, ClassMate, GetClassComment,
                    NewClassComment, Tech, Rent, Shop, EditShop,
                    NewPrivateArticle, CurrentUserShop]
modules_relation = [NewRelation, RemoveRelation]
modules_msg = [CheckMsg, DelMsg, GetMsg, SendMsg]
modules_map = [MapHandler, ViewLastMap]
modules_chat = [ChatMessage, ChatPage]


modules = (modules_master + modules_users + modules_building +
           modules_relation + modules_msg + modules_map + modules_chat)
