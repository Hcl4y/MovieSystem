from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

import time
from datetime import datetime
from django.utils.timezone import make_aware
import json

import math


# huiyuan_fenlei 表：0-id    1-caidan_mingcheng   2-caidan_lujing   3-caidan_jibie   4-caidan_suoshu   5-paixu_id
def huiyuan_fenlei(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        row_edit = ""
        # 如果是修改，则读取要修改的内容
        if id_1ji:
            curson_edit = connection.cursor()
            sql_edit = "select * from huiyuan_fenlei where id=%s" % id_1ji
            curson_edit.execute(sql_edit)
            row_edit = curson_edit.fetchone()

        # 读取所有1级菜单
        curson = connection.cursor()
        curson.execute("select * from huiyuan_fenlei where caidan_jibie=1")
        rows = curson.fetchall()
        neirong = {
            "caidan_1jis": rows,
            "id_1ji": id_1ji,
            "caidan_info": row_edit
        }
        return render(request, "houtai/huiyuan/caidan_1ji.html", context=neirong)

    if request.method == "POST":
        # 判断id_1ji，有值则是修改，没有则是新录入
        id_1ji = request.POST.get("id_1ji")
        if id_1ji:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "update huiyuan_fenlei set caidan_mingcheng='%s',paixu_id=%s where id=%s" % (
                caidan_mingcheng, paixu_id, id_1ji)
            curson.execute(sql)
        else:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "insert into huiyuan_fenlei(caidan_mingcheng,caidan_jibie,caidan_suoshu,paixu_id) values ('%s',1,0,%s)" % (
                caidan_mingcheng, paixu_id)
            curson.execute(sql)
        return redirect("/huiyuan_fenlei")


# 表：0-id    1-caidan_mingcheng   2-caidan_lujing   3-caidan_jibie   4-caidan_suoshu   5-paixu_id
def huiyuan_fenlei_del(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        curson = connection.cursor()
        sql = "delete from huiyuan_fenlei where id=%s" % id_1ji
        curson.execute(sql)
        return redirect("/huiyuan_fenlei")


######################################


# 【huiyuan_fenlei】 0-id  1-caidan_mingcheng  2-caidan_lujing 3-caidan_jibie  4-caidan_suoshu  5-paixu_id
# 【huiyuan】0-id  1-shouji  2-mima  3-fl_id  4-xingming 5-xingbie 6-qq 7-email
#   8-wx_dllx  9-wx_openid  10-wx_nicheng  11-wx_touxiang  12-wx_xingbie  13-wx_riqi 14-wx_shijian
#   15-add_riqi   16-add_shijian  17-beizhu
def huiyuan_list(request, dijiye):
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from huiyuan"
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 10
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    # sql = "select * from kecheng"
    sql = "select * from huiyuan order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据
    # for row in rows:
    #    print(row)

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">注册时间</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">会员账号</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%">会员信息</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="35%">会员简介</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">操作</td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        tmp_leixing = "普通"
        if row[1]:
            pass
        else:
            tmp_leixing = "<b>微信</b>"

        info_putong = ""
        if row[1]:
            info_putong = info_putong + "手机：" + row[1]

        info_weixin = ""
        # if row[9]:
        #     info_weixin = info_weixin + "<img src='%s' height=50>" % row[11]
        #     info_weixin = info_weixin + row[10]

        # 【huiyuan_fenlei】 0-id  1-caidan_mingcheng  2-caidan_lujing 3-caidan_jibie  4-caidan_suoshu  5-paixu_id
        # 【huiyuan】0-id  1-shouji  2-mima  3-fl_id  4-xingming 5-xingbie 6-touxiang 7-qq
        #   8-email  9-jianjie  17-add_riqi  18-add_shijian
        #   15-add_riqi   16-add_shijian  17-beizhu
        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[18]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[1]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">姓名：%s（%s）  <br>QQ：%s <br>Email：%s  </td>' % (
        row[4], row[5], row[7], row[8])
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[9]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        biaoge = biaoge + '<a href="/huiyuan_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
        biaoge = biaoge + '</td>'
        biaoge = biaoge + '</tr>'
    biaoge = biaoge + '</table>'
    caidan = ""

    caidan = caidan + '<a href="0">首页</a>&nbsp;&nbsp;'
    if int(dijiye) >= 1:
        caidan = caidan + '<a href="%s">上一页</a>&nbsp;&nbsp;' % (int(dijiye) - 1)
    else:
        caidan = caidan + '上一页&nbsp;&nbsp;'

    if int(dijiye) >= (int(yeshu) - 1):
        caidan = caidan + '下一页&nbsp;&nbsp;'
    else:
        caidan = caidan + '<a href="%s">下一页</a>&nbsp;&nbsp;' % (int(dijiye) + 1)

    caidan = caidan + '<a href="%s">尾页</a>&nbsp;&nbsp;' % (int(yeshu) - 1)

    caidan = caidan + "&nbsp;&nbsp;总数据：%s | " % zongshuju
    caidan = caidan + "每页：%s | " % meiye
    caidan = caidan + "当前页数：%s | " % (int(dijiye) + 1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge
    }

    return render(request, "houtai/huiyuan/huiyuan_list.html", context=neirong)


def huiyuan_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from huiyuan where id=%s" % id
        curson.execute(sql)
        return redirect("/huiyuan_list/%s" % dijiye)
