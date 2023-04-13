from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime
from django.utils.timezone import make_aware
import json


def kc_list(request):
    curson = connection.cursor()
    curson.execute("select * from web")
    rows = curson.fetchall()
    return render(request, "kc_list.html", context={"kechengs": rows})


def ht(request):
    if request.method == "GET":
        return render(request, "houtai/login.html")
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user_password = request.POST.get("user_password")

        curson = connection.cursor()
        curson.execute(
            "select * from quanxian_yonghu where user_name='%s' and user_password='%s' " % (user_name, user_password))
        info = curson.fetchone()
        print(info)
        print(user_name)
        neirong = {}
        if info:
            if info[0]:
                # 写登录cookie
                shijian01 = datetime(year=2099, month=1, day=1, hour=20, minute=0, second=0)
                shijian02 = make_aware(shijian01)
                # response = HttpResponse("cookie设置")
                response = redirect("/ht/main")
                # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
                response.set_cookie("uid", info[0], expires=shijian01)
                response.set_cookie("uname", info[1], expires=shijian01)
                response.set_cookie("fzid", info[3], expires=shijian01)

                # 读取分组信息
                #  # 0-id  1-fenzu_mingcheng  2-quanxian_1 3-quanxian_2  4-quanxian
                curson_fenzu = connection.cursor()
                sql_fenzu = "select * from quanxian_fenzu where id=%s" % info[3]
                curson_fenzu.execute(sql_fenzu)
                row_fenzu = curson_fenzu.fetchone()
                quanxian1 = row_fenzu[2]
                quanxian2 = row_fenzu[3]
                quanxian3 = row_fenzu[4]

                response.set_cookie("quanxian1", quanxian1, expires=shijian01)
                response.set_cookie("quanxian2", quanxian2, expires=shijian01)
                response.set_cookie("quanxian3", quanxian3, expires=shijian01)

                return response
                # 转发
                # return book_views.index(request)
                # 重定向
                # return HttpResponseRedirect("/ht/main")
            return redirect("/ht/main")
        else:
            cuowu = "<script>alert('账号错误')</script>"
            neirong = {
                "cuowu": cuowu
            }
            return render(request, "houtai/login.html", context=neirong)


def ht_main(request):
    return render(request, "houtai/main.html")


def ht_top(request):
    uid = request.COOKIES.get("uid")
    uname = request.COOKIES.get("uname")
    fzid = request.COOKIES.get("fzid")
    quanxian1 = request.COOKIES.get("quanxian1")

    # 读取所有1级菜单
    curson_1ji = connection.cursor()
    sql_1ji = "select * from quanxian_caidan where caidan_jibie=1 and id in(0%s0)" % quanxian1
    curson_1ji.execute(sql_1ji)
    list1 = curson_1ji.fetchall()
    caidan = ""
    for x in list1:
        # 表：0-id    1-caidan_mingcheng   2-caidan_lujing   3-caidan_jibie   4-caidan_suoshu   5-paixu_id
        caidan = caidan + x[1] + " | "

    neirong = {
        "uid": uid,
        "uname": uname,
        "fzid": fzid,
        "quanxian1": quanxian1,
        "caidan": caidan,
        "list1": list1
    }

    return render(request, "houtai/top.html", context=neirong)


def ht_center(request):
    return render(request, "houtai/center.html")


def ht_down(request):
    return render(request, "houtai/down.html")


def ht_middel(request):
    return render(request, "houtai/middel.html")


def ht_left(request):
    return render(request, "houtai/left.html")


def ht_left2(request):
    id_1ji = request.GET.get("id_1ji")
    mc_1ji = request.GET.get("mc_1ji")

    # print(request.COOKIES.get("quanxian2"))
    # 根据1级菜单的id，获取2级菜单 + 3级菜单
    # 读取该1级菜单下  > 所有2级菜单
    caidan = ""
    curson_2ji = connection.cursor()
    sql_2ji = "select * from quanxian_caidan where caidan_jibie=2 and caidan_suoshu=%s  and id in(0%s0)" % (
        id_1ji, request.COOKIES.get("quanxian2"))
    curson_2ji.execute(sql_2ji)
    list2 = curson_2ji.fetchall()
    if list2:
        for row2 in list2:
            # 表：0-id    1-caidan_mingcheng   2-caidan_lujing   3-caidan_jibie   4-caidan_suoshu   5-paixu_id
            caidan = caidan + "【" + row2[1] + "】<br> "

            # 读取该2级菜单下  > 所有3级菜单
            curson_3ji = connection.cursor()
            sql_3ji = "select * from quanxian_caidan where caidan_jibie=3 and caidan_suoshu=%s and id in(0%s0)" % (
                row2[0], request.COOKIES.get("quanxian3"))
            curson_3ji.execute(sql_3ji)
            list3 = curson_3ji.fetchall()
            if list3:
                for row3 in list3:
                    pass
                    # caidan = caidan + "---<a href='"+row3[2]+"' target='I2'>" + row3[1] + "</a><br>"
                    caidan = caidan + "---<a href='%s' target='I2'>%s</a><br>" % (row3[2], row3[1])
                caidan = caidan + "<hr>"
        # print(caidan)

    neirong = {
        "id_1ji": id_1ji,
        "mc_1ji": mc_1ji,
        "caidan": caidan
    }
    return render(request, "houtai/left2.html", context=neirong)


def ht_tab(request):
    return render(request, "houtai/tab.html")
