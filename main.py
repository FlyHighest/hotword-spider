# -*- coding: utf-8 -*-
import data_utils
import threading
import time

def task():
    timer=threading.Timer(600,task)
    timer.start() 
    du=data_utils.DBUtil()
    du.insert('baidu')
    du.insert('weibo')
    du.insert('zhihu')    
    
task()
