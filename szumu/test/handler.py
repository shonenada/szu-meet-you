'''
Created on 2012-8-16

@author: Lyd
'''

from web import *
from tornado.template import Template
from szumu.building.special import TeachingBuilding
from szumu.users.model import RelationShip

import time

class testHandler(Controller):

    def get(self):
        rs = RelationShip.get_friends_list(self.db, '12')
        print rs
        self.write(json_encode(rs))


    '''    
    def get(self):
        start = time.clock()
        user = self.get_current_user()
        if not user: raise httperror(403)
        user = user.as_array()
        course = TeachingBuilding.get_course_infor_by_truename_and_number(self.db, user['truename'], user['number'])
        classinfor = []
        for x in course:
            classinfor.append(TeachingBuilding.get_course_infor_by_classid(self.db, x['cid']))
        self.write(unicode(classinfor))
        end = time.clock()
        self.write(unicode(start - end))
    '''