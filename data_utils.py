# -*- coding: utf-8 -*-
import pymysql
import configparser
import datetime
import pytz
from spider import get_hotword
from mailnotify import mail
class DBUtil():
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("conf.ini")
        conf = dict(cf.items('database'))
        self.connection = pymysql.connect(host=conf['host'], 
                                     port=int(conf['port']), 
                                     user=conf['user'], 
                                     password=conf['password'], 
                                     db=conf['database'], 
                                     charset=conf['charset'])
        
        self.cursor = self.connection.cursor()
        
    def __del__(self):
        self.connection.close()
        
    def insert(self,table):
        #table: baidu or weibo
        tz = pytz.timezone('Asia/Shanghai')
        create_time=tz.localize(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        
        score,word=get_hotword(table)
        if not score==None:
            for i in range(0,len(score)):
                
                top=0 if table=='weibo' else 1
                
                sql="insert into %s(create_time,word,score,no) values('%s','%s',%d,%d);"%(table,create_time,word[i].encode('utf-8').decode(),int(score[i]),i+top)
                try:
                    self.cursor.execute(sql)
                    self.connection.commit()
                    
                except Exception as e:
                             
                    print(sql)
                    self.connection.rollback()
        else:
            mail(table+' get None list from spider')
 
