from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

import time
from datetime import datetime
from django.utils.timezone import make_aware
import json

import math

#网站设置，网站名称，关键字，描述
def set_web_mc(request):
    if request.method == "GET":
        id = request.GET.get("id")

        curson = connection.cursor()
        curson.execute("select * from web_key where id=%s" % id)
        info = curson.fetchone()
        print(info[3])

        neirong = {
            "info": info,
            "id": id
        }
        return render(request, "houtai/shezhi/set_web_mc.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")

        Mingcheng = request.POST.get("Mingcheng")
        Guanjianzi = request.POST.get("Guanjianzi")
        Miaoshu = request.POST.get("Miaoshu")

        # 0-id  1-Mingcheng  2-Guanjianzi 3-Miaoshu
        curson = connection.cursor()
        sql = "update web_key set Mingcheng='%s',Guanjianzi='%s',Miaoshu='%s'  where id=%s " % (Mingcheng, Guanjianzi, Miaoshu, id)
        curson.execute(sql)
        return redirect("/set_web_mc?id=%s" % id)

#关于我们设置：网站介绍、联系我们、加入我们、法律声明
def set_guanyu_women(request):
    if request.method == "GET":
        id = request.GET.get("id")

        curson = connection.cursor()
        curson.execute("select * from guanyu_women where id=%s" % id)
        info = curson.fetchone()

        neirong = {
            "info": info,
            "id": id
        }
        return render(request, "houtai/shezhi/set_guanyu_women.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")

        neirong = request.POST.get("neirong")

        # 0-id  1-Mingcheng  2-Guanjianzi 3-Miaoshu
        curson = connection.cursor()
        sql = "update guanyu_women set neirong='%s'  where id=%s " % (neirong,id)
        curson.execute(sql)
        return redirect("/set_guanyu_women?id=%s" % id)

#热门关键字设定
def set_key_remen(request):
    if request.method == "GET":
        #id = request.GET.get("id")
        id = 2
        curson = connection.cursor()
        curson.execute("select * from web_key where id=%s" % id)
        info = curson.fetchone()

        neirong = {
            "info": info,
            "id": id
        }
        return render(request, "houtai/shezhi/set_key_remen.html", context=neirong)

    if request.method == "POST":
        #id = request.POST.get("id")
        id = 2
        Mingcheng = request.POST.get("Mingcheng")
        #Guanjianzi = request.POST.get("Guanjianzi")
        #Miaoshu = request.POST.get("Miaoshu")

        # 0-id  1-Mingcheng  2-Guanjianzi 3-Miaoshu
        curson = connection.cursor()
        sql = "update web_key set Mingcheng='%s' where id=%s " % (Mingcheng,  id)
        curson.execute(sql)
        #return redirect("/set_key_remen?id=%s" % id)
        return redirect("/set_key_remen")

# 【guanggao】0-id  1-wz1  2-tpdz1  3-ljdz1  4-wz2 5-tpdz2 6-ljdz2
# 7-wz3   8-tpdz3  9-ljdz3  10-wz4  11-tpdz4  12-ljdz4
def ad_xiugai(request):
    if request.method == "GET":
        id = request.GET.get("id")

        curson = connection.cursor()
        curson.execute("select * from guanggao where id=%s" % id)
        info = curson.fetchone()
        print(info[3])

        neirong = {
            "info": info,
            "id":id
        }
        return render(request, "houtai/guanggao/ad.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")

        wz1 = request.POST.get("wz1")
        tpdz1 = request.POST.get("tpdz1")
        ljdz1 = request.POST.get("ljdz1")

        wz2 = request.POST.get("wz2")
        tpdz2 = request.POST.get("tpdz2")
        ljdz2 = request.POST.get("ljdz2")

        wz3 = request.POST.get("wz3")
        tpdz3 = request.POST.get("tpdz3")
        ljdz3 = request.POST.get("ljdz3")

        wz4 = request.POST.get("wz4")
        tpdz4 = request.POST.get("tpdz4")
        ljdz4 = request.POST.get("ljdz4")


        # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
        curson = connection.cursor()
        sql = "update guanggao set wz1='%s',tpdz1='%s',ljdz1='%s',wz2='%s',tpdz2='%s',ljdz2='%s',wz3='%s',tpdz3='%s',ljdz3='%s',wz4='%s',tpdz4='%s',ljdz4='%s'  where id=%s " % \
              (wz1,tpdz1,ljdz1,wz2,tpdz2,ljdz2,wz3,tpdz3,ljdz3,wz4,tpdz4,ljdz4,id)
        curson.execute(sql)
        return redirect("/ad?id=%s" % id)
