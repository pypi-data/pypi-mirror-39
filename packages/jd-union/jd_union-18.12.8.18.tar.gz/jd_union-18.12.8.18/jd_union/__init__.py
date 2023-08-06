# -*- coding: utf-8 -*-

__version__ = '18.12.8.18'
__author__ = 'play4fun <play4fun@foxmail.com>'

from jd_union.api.base import sign

class appinfo(object):
    def __init__(self,appkey,secret):
        self.appkey = appkey
        self.secret = secret
        
def getDefaultAppInfo():
    pass

     
def setDefaultAppInfo(appkey,secret):
    default = appinfo(appkey,secret)
    global getDefaultAppInfo 
    getDefaultAppInfo = lambda: default
    




    

