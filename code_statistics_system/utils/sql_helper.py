# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/3/11 18:31
from settings import Config
import pymysql

class SqlHelper(object):

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = Config.POOL.connection()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def fetchone(self,sql,params):
        self.connect()
        self.cursor.execute(sql,params)
        data = self.cursor.fetchone()
        self.close()
        return data

    def fetchmany(self,sql,params,amount):
        self.connect()
        self.cursor.execute(sql, params)
        data = self.cursor.fetchmany(amount)
        self.close()
        return data

    def fetchall(self,sql, params):
        self.connect()
        self.cursor.execute(sql, params)
        data = self.cursor.fetchall()
        self.close()
        return data

    def insert(self,sql,params):
        self.connect()
        self.cursor.execute(sql, params)
        self.conn.commit()
        self.close()

    def close(self):
        self.cursor.close()
        self.conn.close()

helper = SqlHelper()