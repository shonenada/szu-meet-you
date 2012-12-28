#!/usr/bin/env python

import os.path

from UnitTest import test

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from config.webConfig import Config

import szumu.home.handler as home
import szumu.users.hanlder as users
import szumu.chat.handler as chat
import szumu.master.infor as infor
import szumu.map.handler as map
import szumu.building.shop.handler as shop
import szumu.building.handler as building

import szumu.test.handler as test

define("port", default=Config.getWebPort(), help="run on the given port", type=int)
define("mysql_host", default=Config.getDbHost()+":"+Config.getDbPort(), help="database host")
define("mysql_database", default=Config.getDbDatabase(), help="database name")
define("mysql_user", default=Config.getDbUser(), help="database user")
define("mysql_password", default=Config.getDbPasswd(), help="database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", home.HomeHandler),
            (r"/auth/reg", users.UserSignUpHandler),
            (r"/auth/login", users.UserLoginHandler),
            (r"/auth/logout", users.UserLogOutHandler),
            
            (r"/home", users.MyHomeHandler),
            (r"/account/profile", users.ProfileHandler),
            (r"/account/myshop", shop.CurrentUserShopHandler),
            (r"/account/msg/check", users.MsgCheckHandler),
            (r"/account/msg/get/(send|receive)/", users.MsgGetHandler),
            (r"/account/msg/del/(send|receive)", users.MsgDelHandler),
            (r"/account/msg/send", users.MsgSendHandler),
            (r"/account/msg/re", users.MsgReHandler),
            (r"/account/userinfor/get/([0-9]+)", users.UserInforGetHandler),
            (r'/account/relation/friend/new/([0-9]+)', users.NewRelationshipHandler),
            (r'/account/relation/friend/remove/([0-9]+)', users.RemoveRelationshipHandler),
            
            (r"/map", map.ViewLastMapHandler),
            (r"/map/([0-9]+)", map.MapHandler),
            
            (r"/office", building.OfficeHandler),
            (r"/office/student/reg", users.OfficeHandler),
            (r"/teach", building.TeachHandler),

            (r"/teach/mate/classid/([0-9]+)", building.ClassMateHandler),
            (r"/teach/comment/classid/([0-9]+)", building.ClassCommentGetHandler),
            (r"/teach/comment/new", building.ClassCommentNewHandler),

            (r"/shop/(private|topic|sell)/([0-9]+)", building.ShopHandler),
            (r"/shop/edit", building.ShopEditHandler),

            (r"/shop/private/article/new/([0-9]+)", building.PrivateNewArticleHandler),
            (r"/shop/private/article/del", building.PrivateDelArticleHandler),

            (r"/tech", building.TechHandler),
            (r"/north", building.NorthHandler),
            (r"/south",  building.SouthHandler),
            (r"/litera",  building.LiteraHandler),
            (r"/student",  building.StudentHandler),
            (r"/stone",  building.StoneHandler),
            (r"/gym",  building.GymHandler),
            (r"/dorm/([0-9]+)", building.DormHandler),
            (r"/rent/([0-9]+)", building.RentHandler),            
            
            (r"/chat", chat.ChatPageHandler),
            (r"/chat/messages", chat.ChatMessageHandler),
            
            (r"/infor/aboutus", infor.AboutHandler),
            (r"/infor/contactus", infor.ContactHandler),
            
            (r"/test/", test.testHandler),
        ]
        settings = dict(
            title=u"Szu_MeetYou",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
   #        ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="1non23o5nonwfi23fn0aw3nfv03nv023v023v/wetgq=",
            login_url="/auth/login",
            autoescape=None,
            debug=True,
            
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(),xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


