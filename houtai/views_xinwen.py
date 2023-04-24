from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

import time
from datetime import datetime
from django.utils.timezone import make_aware
import json

import math


# 热门关键字设定
def set_key_remen_xinwen(request):
    if request.method == "GET":
        # id = request.GET.get("id")
        id = 2
        curson = connection.cursor()
        curson.execute("select * from web_key where id=%s" % id)
        info = curson.fetchone()

        neirong = {
            "info": info,
            "id": id
        }
        return render(request, "houtai/xinwen/set_key_remen_xinwen.html", context=neirong)
    if request.method == "POST":
        # id = request.POST.get("id")
        id = 2
        Mingcheng = request.POST.get("Mingcheng")
        # Guanjianzi = request.POST.get("Guanjianzi")
        # Miaoshu = request.POST.get("Miaoshu")

        # 0-id  1-Mingcheng  2-Guanjianzi 3-Miaoshu
        curson = connection.cursor()
        sql = "update web_key set Mingcheng='%s' where id=%s " % (Mingcheng, id)
        curson.execute(sql)
        # return redirect("/set_key_remen?id=%s" % id)
        return redirect("/set_key_remen_xinwen")


def xinwen_fenlei(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        row_edit = ""
        # 如果是修改，则读取要修改的内容
        if id_1ji:
            curson_edit = connection.cursor()
            sql_edit = "select * from xinwen_fenlei where id=%s" % id_1ji
            curson_edit.execute(sql_edit)
            row_edit = curson_edit.fetchone()

        # 读取所有1级菜单
        curson = connection.cursor()
        curson.execute("select * from xinwen_fenlei where caidan_jibie=1")
        rows = curson.fetchall()
        neirong = {
            "caidan_1jis": rows,
            "id_1ji": id_1ji,
            "caidan_info": row_edit
        }
        return render(request, "houtai/xinwen/caidan_1ji.html", context=neirong)

    if request.method == "POST":
        # 判断id_1ji，有值则是修改，没有则是新录入
        id_1ji = request.POST.get("id_1ji")
        if id_1ji:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "update xinwen_fenlei set caidan_mingcheng='%s',paixu_id=%s where id=%s" % (
                caidan_mingcheng, paixu_id, id_1ji)
            curson.execute(sql)
        else:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "insert into xinwen_fenlei(caidan_mingcheng,caidan_jibie,caidan_suoshu,paixu_id) values ('%s',1,0,%s)" % (
                caidan_mingcheng, paixu_id)
            curson.execute(sql)
        return redirect("/xinwen_fenlei")


# 表：0-id    1-caidan_mingcheng   2-caidan_lujing   3-caidan_jibie   4-caidan_suoshu   5-paixu_id
def xinwen_fenlei_del(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        curson = connection.cursor()
        sql = "delete from xinwen_fenlei where id=%s" % id_1ji
        curson.execute(sql)
        return redirect("/xinwen_fenlei")


######################################

def xinwen_add(request):
    if request.method == "GET":
        # 【xinwen_fenlei】 0-id  1-caidan_mingcheng  2-caidan_lujing 3-caidan_jibie  4-caidan_suoshu  5-paixu_id
        # 【xinwen】0-id  1-xinxi_lxid1  2-xinxi_lxid2  3-xinxi_biaoti  4-xinxi_riqi 5-xinxi_jianjie_yn 6-xinxi_jianjie
        # 7-xinxi_tupian_yn   8-xinxi_tupian  9-xinxi_ding  10-xinxi_neirong  11-add_riqi  12-add_shijian
        curson = connection.cursor()
        curson.execute("select * from xinwen_fenlei ")
        fenzus = curson.fetchall()
        neirong = {
            "fenzus": fenzus
        }
        return render(request, "houtai/xinwen/xinwen_add.html", context=neirong)

    if request.method == "POST":
        xinxi_lxid = request.POST.get("xinxi_lxid")
        xinxi_biaoti = request.POST.get("xinxi_biaoti")
        xinxi_riqi = request.POST.get("xinxi_riqi")

        xinxi_jianjie_yn = request.POST.get("jianjie_yn")
        if xinxi_jianjie_yn == "on":
            xinxi_jianjie_yn = 1
        else:
            xinxi_jianjie_yn = 0
        xinxi_jianjie = request.POST.get("xinxi_jianjie")

        xinxi_tupian_yn = request.POST.get("tupian_yn")
        if xinxi_tupian_yn == "on":
            xinxi_tupian_yn = 1
        else:
            xinxi_tupian_yn = 0
        xinxi_tupian = request.POST.get("xinxi_tupian")

        xinxi_neirong = request.POST.get("xinxi_neirong")

        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        curson = connection.cursor()
        sql = "insert into xinwen(xinxi_lxid1,xinxi_biaoti,xinxi_riqi,xinxi_jianjie_yn,xinxi_jianjie,xinxi_tupian_yn,xinxi_tupian,xinxi_neirong,add_riqi,add_shijian) " \
              "values (%s,'%s','%s',%s,'%s',%s,'%s','%s','%s','%s')" \
              % (xinxi_lxid, xinxi_biaoti, xinxi_riqi, xinxi_jianjie_yn, xinxi_jianjie, xinxi_tupian_yn, xinxi_tupian,
                 xinxi_neirong, add_riqi, add_shijian)
        curson.execute(sql)
        return redirect("/xinwen_list/0")


# 新闻列表
# 【xinwen_fenlei】 0-id  1-caidan_mingcheng  2-caidan_lujing 3-caidan_jibie  4-caidan_suoshu  5-paixu_id
# 【xinwen】0-id  1-xinxi_lxid1  2-xinxi_lxid2  3-xinxi_biaoti  4-xinxi_riqi 5-xinxi_jianjie_yn 6-xinxi_jianjie
# 7-xinxi_tupian_yn   8-xinxi_tupian  9-xinxi_ding  10-xinxi_neirong  11-add_riqi  12-add_shijian
def xinwen_xiugai(request):
    if request.method == "GET":
        # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
        curson_fenzu = connection.cursor()
        curson_fenzu.execute("select * from xinwen_fenlei")
        fenzus = curson_fenzu.fetchall()

        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        curson.execute("select * from xinwen where id=%s" % id)
        info = curson.fetchone()
        print(info[3])

        neirong = {
            "fenzus": fenzus,
            "info": info,
            "fzid": info[1],
            "dijiye": dijiye
        }
        return render(request, "houtai/xinwen/xinwen_xiugai.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")
        dijiye = request.POST.get("dijiye")

        xinxi_lxid = request.POST.get("xinxi_lxid")
        xinxi_biaoti = request.POST.get("xinxi_biaoti")
        xinxi_riqi = request.POST.get("xinxi_riqi")

        xinxi_jianjie_yn = request.POST.get("jianjie_yn")
        if xinxi_jianjie_yn == "on":
            xinxi_jianjie_yn = 1
        else:
            xinxi_jianjie_yn = 0
        xinxi_jianjie = request.POST.get("xinxi_jianjie")

        xinxi_tupian_yn = request.POST.get("tupian_yn")
        if xinxi_tupian_yn == "on":
            xinxi_tupian_yn = 1
        else:
            xinxi_tupian_yn = 0
        xinxi_tupian = request.POST.get("xinxi_tupian")

        xinxi_neirong = request.POST.get("xinxi_neirong")

        # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
        curson = connection.cursor()
        sql = "update xinwen set xinxi_lxid1=%s,xinxi_biaoti='%s',xinxi_riqi='%s',xinxi_jianjie_yn=%s,xinxi_jianjie='%s'," \
              "xinxi_tupian_yn=%s,xinxi_tupian='%s',xinxi_neirong='%s' where id=%s" % \
              (xinxi_lxid, xinxi_biaoti, xinxi_riqi, xinxi_jianjie_yn, xinxi_jianjie, xinxi_tupian_yn, xinxi_tupian,
               xinxi_neirong, id)
        curson.execute(sql)
        return redirect("/xinwen_list/%s" % dijiye)


# 新闻列表
# 【xinwen_fenlei】 0-id  1-caidan_mingcheng  2-caidan_lujing 3-caidan_jibie  4-caidan_suoshu  5-paixu_id
# 【xinwen】0-id  1-xinxi_lxid1  2-xinxi_lxid2  3-xinxi_biaoti  4-xinxi_riqi 5-xinxi_jianjie_yn 6-xinxi_jianjie
# 7-xinxi_tupian_yn   8-xinxi_tupian  9-xinxi_ding  10-xinxi_neirong  11-add_riqi  12-add_shijian

def xinwen_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from xinwen where id=%s" % id
        curson.execute(sql)
        return redirect("/xinwen_list/%s" % dijiye)


# 新闻列表
# 【xinwen_fenlei】 0-id  1-caidan_mingcheng  2-caidan_lujing 3-caidan_jibie  4-caidan_suoshu  5-paixu_id
# 【xinwen】0-id  1-xinxi_lxid1  2-xinxi_lxid2  3-xinxi_biaoti  4-xinxi_riqi 5-xinxi_jianjie_yn 6-xinxi_jianjie
# 7-xinxi_tupian_yn   8-xinxi_tupian  9-xinxi_ding  10-xinxi_neirong  11-add_riqi  12-add_shijian
def xinwen_list(request, dijiye):
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xinwen"
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    # sql = "select * from kecheng"
    sql = "select * from xinwen order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据
    # for row in rows:
    #    print(row)

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">时间</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="40%">标题</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">类型</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">推荐</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">缩略图</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">操作</td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        tmp_leixing = ""

        tmp_tuijian = ""
        if row[5] == 1:
            tmp_tuijian = "有"
        print(tmp_tuijian)

        tmp_tupian = ""
        if row[7] == 1:
            tmp_tupian = "有"

        curson = connection.cursor()
        curson.execute("select * from xinwen_fenlei where id=%s" % row[1])
        tmp_leixing = curson.fetchone()

        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[11]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[3]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % tmp_leixing[1]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % tmp_tuijian
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % tmp_tupian
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        biaoge = biaoge + '<a href="/xinwen_xiugai?id=%s&dijiye=%s">修改</a>&nbsp;&nbsp;' % (row[0], dijiye)
        biaoge = biaoge + '| &nbsp;&nbsp;<a href="/xinwen_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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

    return render(request, "houtai/xinwen/xinwen_list.html", context=neirong)


# 评论列表
def xinwen_pinglun_list(request, dijiye):
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xinwen_pinglun"
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select * from xinwen_pinglun order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">评论时间</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">会员</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="25%">内容</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="25%">状态 | 操作</td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        huiyuan = ""
        curson_huiyuan = connection.cursor()
        curson_huiyuan.execute("select * from huiyuan where id=%s" % row[1])
        tmp_huiyuan = curson_huiyuan.fetchone()
        print(tmp_huiyuan[0])
        # if tmp_huiyuan[6]:
        #      huiyuan =  huiyuan + "<img src="+ tmp_huiyuan[6] +" height=50><br>" + tmp_huiyuan[10]
        # else:
        huiyuan = huiyuan + tmp_huiyuan[1]

        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[5]  # 评论时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % huiyuan  # 会员信息
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[3]  # 内容

        biaoge = biaoge + '<td bgcolor="#FFFFFF">'  # 订单状态 + 处理
        # 1在购物车，还没下单；2下单，没有付款；3已经付款，还没发货；4已经发货，等待客户收货；5客户收货
        # biaoge = biaoge + str(row[7])
        if row[6] == 0:
            biaoge = biaoge + "0-等待审核 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            biaoge = biaoge + '<a href="/xinwen_pinglun_chuli?id=%s&dijiye=%s">评论处理</a>' % (row[0], dijiye)
        if row[6] == 1:
            biaoge = biaoge + "1-审核拒绝 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            biaoge = biaoge + '<a href="/xinwen_pinglun_chuli?id=%s&dijiye=%s">评论处理</a>' % (row[0], dijiye)
        if row[6] == 2:
            biaoge = biaoge + "2-审核通过 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            biaoge = biaoge + '<a href="/xinwen_pinglun_chuli?id=%s&dijiye=%s">评论处理</a>' % (row[0], dijiye)

        biaoge = biaoge + '</td>'
        biaoge = biaoge + '</tr>'
        biaoge = biaoge + '<tr><td colspan=6  style="padding:1px" bgcolor="gray"></td></tr>'

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

    return render(request, "houtai/xinwen/xinwen_pinglun_list.html", context=neirong)


# 评论处理
def xinwen_pinglun_chuli(request):
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        curson.execute("select * from xinwen_pinglun where id=%s" % id)
        info = curson.fetchone()

        neirong = {
            "id": id,
            "dijiye": dijiye,
            "yn_shenhe": info[5],
            "shenhe_beizhu": info[6]
        }
        return render(request, "houtai/xinwen/xinwen_pinglun_chuli.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")
        dijiye = request.POST.get("dijiye")

        yn_shenhe = request.POST.get("yn_shenhe")
        shenhe_beizhu = request.POST.get("shenhe_beizhu")

        # 【gouwuche】0-id  1-u_id  2-u_ip  3-cp_id  4-cp_mingcheng 5-jiage_shichang 6-jiage_chengjiao
        # 7-cp_shuliang   8-zt  9-shijian_gouwuche  10-shijian_xiadan  11-shijian_fukuan
        # 12-shijian_fahuo  13-shijian_shouhuo  14-danhao  15-pinglun_yn  16-pinglun_id

        # 【dingdan】0-id  1-danhao  2-u_id  3-u_ip  4-dizhi_id 5-beizhu_dingdan 6-feiyong_chengjiao
        # 7-zt   8-shijian_xiadan  9-shijian_fukuan  10-shijian_fahuo  11-shijian_shouhuo
        # 12-beizhu_fahuo  13-beizhu_caozuo  14-pinglun_yn  15-pinglun_id
        curson = connection.cursor()
        sql = "update xinwen_pinglun set yn_shenhe=%s,shenhe_beizhu='%s' where id=%s" % \
              (yn_shenhe, shenhe_beizhu, id)
        curson.execute(sql)
        return redirect("/xinwen_pinglun_list/%s" % dijiye)
