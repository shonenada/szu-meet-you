#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tornado import database
from config.webConfig import Config

class dbMaster(object):
    
    __table = None
    __columns = []
    __values = []
    __where = []
    __query = None
    
    __udpate_new = []
    
    __query_type = None
    __query_type_select = "SELECT"
    __query_type_insert = "INSERT"
    __query_type_update = "UPDATE"
    __query_type_delete = "DELETE"
    
    
    def __init__(self, host=None, database=None, prefix=None, user=None, passwd=None, charset=None):
        if host == None:
            self.host = Config.getDbHost()
        if database == None:
            self.database = Config.getDbDatabase()
        if prefix == None:
            self.prefix = Config.getDbPrefix()
        if user == None:
            self.user = Config.getDbUser()
        if passwd == None:
            self.passwd = Config.getDbPasswd()
        if charset == None:
            self.charset = Config.getDbCharset()
        self.resetdb = False
        self.db = None
        return self
    
    def __del__(self):
        if self.db:
            self.db.close()

    def connect(self):
        """ Connect with database """
        if not self.db and not self.resetdb:
            self.db = database.Connection(host=self.host, database=self.database, user=self.user, password=self.passwd)
        return self.db
            
    def reset_db(self, host=None, database=None, user=None, passwd=None, charset=None):
        """ Reconnect the database """
        self.__init__(host, database, user, passwd, charset)
        self.resetdb = True
        self.connet()

    def set_table(self,table):
        """ Set the query table """
        if not self.db:
            raise "No database connected."
        self.__table = Config.getDbPrefix() + table
        
    def set_columns(self, columns):
        self.__columns = [ x for x in columns]
        
    def set_values(self, values):
        self.__columns = [ x for x in values]
    
    def select(self, columns):
        self.__query_type = self.__query_type_select
        self.set_columns(columns)
        return self

    def where(self, column, op, value, type=None):
        self.__where.append([column, op, value, type])
    
    def and_where(self, column, op, value):
        self.__where(column, op, value, "and")
        
    def or_where(self, column, op, value):
        self.__where(column, op, value, 'or')

    def insert(self, table, columns, values):
        """ Insert a data list into the database. """
        if not len(columns) == len(values):
            return "No equality for the numbers of columns and values."  
        self.__query_type = self.__query_type_insert
        self.set_table(table)
        self.set_columns(columns)
        self.set_values(values)
        return self
    
    def update(self, table, new_columns, new_values):
        """ Update the data """
        if not len(new_columns) == len(new_values):
            return "No equality for the number of columns and values."
        self.__query_type = self.__query_type_update
        self.set_table(table)
        for x in range(len(new_columns)):
            self.__update_new.append([ new_columns[x], new_values[x]])
        return self
        
    def delete(self, table, columns, values):
        """ Delete a record """
        if not len(columns) == len(values):
            return "No equality for the number of columns and values."
        self.__query_type = self.__query_type_delete
        self.set_table(table)
        self.set_columns(columns)
        self.set_values(values)
        return self
        
    def compile(self):
        """ Compile the SQL query """
        if not self.__query_type:
            return "Wrong value of query type."
        if not self.__table:
            return "Wrong table value."
        if len(self.__columns) == 0 :
            return "None of columns."
        if len(self.__values) == 0 :
            return "None of values."
        if not len(self.__columns) == len(self.__values):
            return "No equality for the numbers of columns and values."
        if self.__query_type == self.__query_type_select:
            self.__query = self.__query_type
            self.column = [ x+',' for x in self.__columns]
            self.column[len(self.column)-1] = self.__columns[len(self.__columns)-1]
            self.__query = self.__query + ''.join(self.column)
            self.__query = self.__query + " FROM " + self.table
            if not len(self.__where) == 0:
                self.__query = self.__query + " WHERE " 
                self.__where[0][3] = None
                self.__where[len(self.__where-1)][3] = None
                for x in self.__where:
                    self.__query = self.__query + x[3] + x[0] + x[1] + x[2]
                    
        if self.__query_type == self.__query_type_insert:
            self.__c = [x+',' for x in self.__columns]
            self.__c[len(self.__c)-1] = self.__columns[len(self.__columns)-1]
            
            self.__v = [x+',' for x in self.__values]
            self.__v[len(self.__v)-1] = self.__columns[len(self.__values)-1]
            
            self.__query = self.__query_type + self.__table + " ( " + ''.join(self.__c) + ") VALUES ( "  + ''.join(self.__v) + " ) " 
    
        if self.__query_type == self.__query_type_update:
            if not len(self.__update_new_columns) == len(self.__update_new_values):
                return "No equality for the number of columns and values."
            if len(self.__update_new_columns) == 0 or len(self.__update_new_values) == 0 :
                return 'None of the columns and values.'
            self.__u = [ x[0] +'=' + x[1] + ',' for x in self.__update_new]
            self.__u[len(self.__u)-1] = self.__update_new[len(self.__update_new)-1][0] + '=' + self.__update_new[len(self.__update_new)-1][1] 
            self.__query = self.__query_type + ' ' + self.__table + ' SET ' + ''.join(self.__u) + ' WHERE '
            if not len(self.__where) == 0:
                self.__where[0][3] = None
                self.__where[len(self.__where-1)][3] = None
                for x in self.__where:
                    self.__query = self.__query + x[3] + x[0] + x[1] + x[2]
        
        if self.__query_type == self.__query_type_delete:
            self.__query = self.__query_type + ' FROM ' + self.__table + ' WHERE '
            if not len(self.__where) == 0:
                self.__where[0][3] = None
                self.__where[len(self.__where-1)][3] = None
                for x in self.__where:
                    self.__query = self.__query + x[3] + x[0] + x[1] + x[2]
                
    
    def execute(self):
        if self.__query_type == self.__query_type_select :
            return self.db.query(self.__query)
        else:
            return self.db.execute(self.__query)
        
        
        
        
        
    
    
            
