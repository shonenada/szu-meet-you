'''
Created on 2012-7-27

@author: Lyd
'''
class Config(object):

    __szumu_web_port = 8888

    __szumu_auth_salt = "TYAWawe9ia3n2naw39293ngjaw/at3q0"
    __szumu_token_salt = '^#$DFE%$T^%^%$F21sd$#sdfw3/32t'

    __szumu_db_host = "localhost"
    __szumu_db_port = '3306'
    __szumu_db_prefix = "szu_mu_"
    __szumu_db_database = "szumeetu"
    __szumu_db_user = "root"
    __szumu_db_passwd = ""
    __szumu_db_charset = "utf8"

    @staticmethod
    def getWebPort():
        return Config.__szumu_web_port

    @staticmethod
    def getSalt():
        return Config.__szumu_auth_salt

    @staticmethod
    def get_token_salt():
        return Config.__szumu_token_salt

    @staticmethod
    def getDbPort():
        return Config.__szumu_db_port

    @staticmethod
    def getDbHost():
        return Config.__szumu_db_host

    @staticmethod
    def getDbPrefix():
        return Config.__szumu_db_prefix

    @staticmethod
    def getDbDatabase():
        return Config.__szumu_db_database

    @staticmethod
    def getDbUser():
        return Config.__szumu_db_user

    @staticmethod
    def getDbPasswd():
        return Config.__szumu_db_passwd

    @staticmethod
    def getDbCharset():
        return Config.__szumu_db_charset
