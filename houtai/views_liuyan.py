from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

import time
from datetime import datetime
from django.utils.timezone import make_aware
import json

import math


def liuyan_del(request):
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from liuyan where id=%s" % id
        curson.execute(sql)
        return redirect("/liuyan_list/%s" % dijiye)


# 【liuyan】 0-id  1-xingming  2-dianhua 3-youxiang  4-zhuti  5-neirong  6-add_date
def liuyan_list(request, dijiye):
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from liuyan"
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)
    cursor = connection.cursor()
    # sql = "select * from kecheng"
    sql = "select * from liuyan order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据
    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">时间</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">标题</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="25%">内容</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="40%">联系人/手机/邮箱</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">操作</td>'
    biaoge = biaoge + '</tr>'
    for row in rows:
        # 【liuyan】 0-id  1-xingming  2-dianhua 3-youxiang  4-zhuti  5-neirong  6-add_date
        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[6]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[4]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[5]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s/%s/%s</td>' % (row[1], row[2], row[3])
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        biaoge = biaoge + '<a href="/liuyan_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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

    return render(request, "houtai/qita/liuyan_list.html", context=neirong)
