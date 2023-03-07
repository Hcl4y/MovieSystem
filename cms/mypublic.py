import math

from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse

from datetime import  datetime
from django.utils.timezone import make_aware
import json
import time

# https://www.cnblogs.com/meitian/p/6557344.html 参考资料
#获取公用的cookie
def uname(request):
    h_id = request.COOKIES.get("h_id")
    h_name = request.COOKIES.get("h_name")
    return {'h_id': h_id,'h_name':h_name}

#获取 资讯 分类
def zixun_fenlei(request):
    #读取最新上架商品
    curson_zixun_fenlei= connection.cursor()
    curson_zixun_fenlei.execute("select id,caidan_mingcheng from xinwen_fenlei")
    rows_zixun_fenlei = curson_zixun_fenlei.fetchall()

    neirong = {
        "rows_zixun_fenlei": rows_zixun_fenlei
    }
    return neirong

#获取网站设置
def myweb_key(request):
    curson_web= connection.cursor()
    curson_web.execute("select * from web_key where id=1")
    rows_web = curson_web.fetchone()
    neirong = {
        "myweb_key": rows_web
    }
    return neirong

#获取热门关键字
def remen_key(request):
    curson_web= connection.cursor()
    curson_web.execute("select Mingcheng from web_key where id=2")
    rows_web = curson_web.fetchone()
    print(rows_web[0])
    arr_key = [ x.strip() for x in rows_web[0].split('，') ]

    neirong = {
        "remen_key": arr_key
    }
    return neirong

