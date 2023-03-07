import math

from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

from datetime import datetime
from django.utils.timezone import make_aware
import json
import time


# 资讯信息 首页
def zixun_index(request):
    # 读取广告图片
    # 【guanggao】0-id  1-wz1  2-tpdz1  3-ljdz1  4-wz2 5-tpdz2 6-ljdz2
    # 7-wz3   8-tpdz3  9-ljdz3  10-wz4  11-tpdz4  12-ljdz4
    curson_ad = connection.cursor()
    curson_ad.execute("select * from guanggao where id=1")
    info_ad = curson_ad.fetchone()

    # 读取热门信息
    curson_zixun_remen = connection.cursor()
    curson_zixun_remen.execute("select  id,xinxi_biaoti,add_riqi  from xinwen order by id desc limit 12 ")
    rows_zixun_remen = curson_zixun_remen.fetchall()

    # 读取热门评论信息
    curson_zixun_pinglun = connection.cursor()
    curson_zixun_pinglun.execute(
        "select  pl.riqi,pl.neirong,xw.id  from xinwen_pinglun as pl,xinwen  as xw  where pl.yn_shenhe=2 and  pl.zixun_id = xw.id order by id desc limit 3 ")
    rows_zixun_pinglun = curson_zixun_pinglun.fetchall()
    # print(rows_zixun_pinglun)

    # 读取所有资讯分类
    curson_zixun_fenlei = connection.cursor()
    curson_zixun_fenlei.execute("select id,caidan_mingcheng from xinwen_fenlei")
    rows_zixun_fenlei = curson_zixun_fenlei.fetchall()

    zixuns = ()  # 每个资讯分类 最新6条资讯 集合
    for zixun_fenlei in rows_zixun_fenlei:  # 循环每个分类id
        # 按分类读取最新的6条资讯
        curson_zixun_zuixin = connection.cursor()
        curson_zixun_zuixin.execute(
            "select id,xinxi_lxid1,xinxi_biaoti,xinxi_riqi from xinwen where xinxi_lxid1=%s order by id desc limit 5" %
            zixun_fenlei[0])
        rows_zixun_zuixin = curson_zixun_zuixin.fetchall()
        zixuns = zixuns + rows_zixun_zuixin  # 读取每个分类的最新5个商品【推荐】

    neirong = {
        "ad": info_ad,
        "rows_zixun_remen": rows_zixun_remen,
        "rows_zixun_fenlei": rows_zixun_fenlei,
        "zixuns": zixuns,
        "rows_zixun_pinglun": rows_zixun_pinglun

    }

    return render(request, "pc/zixun_index.html", context=neirong)


# 用户 资讯 收藏
def api_zixun_shoucang(request):
    zixun_id = request.GET.get("zxid")
    u_id = request.GET.get("h_id")
    # print("要收藏的资讯id=%s,用户id=%s" % (zixun_id, u_id))

    # 判断是否收藏，如果没有收藏，则写入数据库
    curson = connection.cursor()
    curson.execute("select * from xinwen_shoucang where zixun_id='%s' and u_id='%s' " % (zixun_id, u_id))
    info = curson.fetchone()
    cuowu = ""
    if info:
        cuowu = "<script>alert('已经收藏')</script>"
    else:
        # #写入数据库
        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        curson_insert = connection.cursor()
        sql_insert = "insert into xinwen_shoucang(zixun_id,u_id,riqi,shijian) values ('%s','%s','%s','%s')" % (
        zixun_id, u_id, add_riqi, add_shijian)
        curson_insert.execute(sql_insert)
        cuowu = "<script>alert('收藏成功')</script>"
    return HttpResponse(cuowu)


# 用户 资讯 提交评论
def api_zixun_pinglun_add(request):
    zixun_id = request.GET.get("zxid")  # 商品id
    h_id = request.GET.get("h_id")  # 会员id
    neirong = request.GET.get("neirong")  # 评论内容

    # 判断是否评论，如果没有，则写入数据库
    curson = connection.cursor()
    curson.execute("select * from xinwen_pinglun where u_id=%s and zixun_id=%s " % (h_id, zixun_id))
    info = curson.fetchone()
    cuowu = ""
    if info:
        cuowu = "<script>alert('您已经提交过评论')</script>"
    else:
        # #写入数据库
        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        curson_insert = connection.cursor()
        sql_insert = "insert into xinwen_pinglun(neirong,u_id,zixun_id,riqi,shijian) values ('%s',%s,%s,'%s','%s')" % (
        neirong, h_id, zixun_id, add_riqi, add_shijian)
        curson_insert.execute(sql_insert)
        cuowu = "<script>alert('您的评论已经提交，审核后显示！')</script>"
    return HttpResponse(cuowu)


# 资讯 收藏 删除
def mem_zixun_shoucang_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from xinwen_shoucang where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_zixun_shoucang_list/%s" % dijiye)


# 资讯 收藏 列表
def mem_zixun_shoucang_list(request, dijiye):
    h_id = request.COOKIES.get("h_id")  # 登录的用户id
    # print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xinwen_shoucang where u_id=%s" % h_id
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    # print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    # print("每页数据 =%s 条" % meiye)
    # print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select  sc.id as scid,sc.riqi,xw.id as xwid,xw.xinxi_biaoti from xinwen_shoucang as sc,xinwen as xw " \
          "where sc.zixun_id=xw.id and sc.u_id=%s  order by sc.id desc limit %s,%s" % (
          h_id, int(meiye) * int(dijiye), meiye)
    # print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%" height="27">收藏日期</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="60%">标题</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%"></td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' % row[1]  # 评论时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/xinxi_xiangqing?zxid=%s" target="_blank">%s</a></td>' % (
        row[2], row[3])  # 会员信息
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'  # 订单状态 + 处理
        biaoge = biaoge + '<a href="/mem_zixun_shoucang_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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
    return render(request, "pc/mem_zixun_shoucang_list.html", context=neirong)


# 资讯 评论 删除
def mem_zixun_pinglun_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from xinwen_pinglun where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_zixun_pinglun_list/%s" % dijiye)


# 资讯 评论 列表
def mem_zixun_pinglun_list(request, dijiye):
    h_id = request.COOKIES.get("h_id")  # 登录的用户id
    # print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xinwen_pinglun where u_id=%s" % h_id
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    # print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    # print("每页数据 =%s 条" % meiye)
    # print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select  pinglun.id as plid,pinglun.riqi,pinglun.neirong,pinglun.yn_shenhe,xw.id as xwid,xw.xinxi_biaoti from xinwen_pinglun as pinglun,xinwen as xw " \
          "where pinglun.zixun_id=xw.id and pinglun.u_id=%s  order by pinglun.id desc limit %s,%s" % (
          h_id, int(meiye) * int(dijiye), meiye)
    # print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%" height="27">评论日期</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="30%">标题</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="35%">评论内容</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">评论状态</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">操作</td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' % row[1]  # 评论时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/xinxi_xiangqing?zxid=%s" target="_blank">%s</a></td>' % (
        row[4], row[5])  # 会员信息
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' % row[2]  # 评论时间

        biaoge = biaoge + '<td bgcolor="#FFFFFF">'  # 订单状态 + 处理
        if row[3] == 0:
            biaoge = biaoge + '状态：待审核'
        if row[3] == 1:
            biaoge = biaoge + '状态：拒绝'
        if row[3] == 2:
            biaoge = biaoge + '状态：已通过'
        biaoge = biaoge + '</td>'

        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        if row[3] == 0:
            biaoge = biaoge + '<a href="/mem_zixun_pinglun_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
        if row[3] == 1:
            biaoge = biaoge + '<a href="/mem_zixun_pinglun_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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
    return render(request, "pc/mem_zixun_pinglun_list.html", context=neirong)


# 资讯 浏览 删除
def mem_zixun_liulan_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from xinwen_liulan where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_zixun_liulan_list/%s" % dijiye)


# 资讯 浏览 列表
def mem_zixun_liulan_list(request, dijiye):
    h_id = request.COOKIES.get("h_id")  # 登录的用户id
    # print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xinwen_liulan where u_id=%s" % h_id
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    # print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    # print("每页数据 =%s 条" % meiye)
    # print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select  liulan.id as llid,liulan.riqi,xw.id as xwid,xw.xinxi_biaoti from xinwen_liulan as liulan,xinwen as xw " \
          "where liulan.zixun_id=xw.id and liulan.u_id=%s  order by liulan.id desc limit %s,%s" % (
          h_id, int(meiye) * int(dijiye), meiye)
    # print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%" height="27">浏览日期</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="60%">标题</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%"></td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' % row[1]  # 评论时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/xinxi_xiangqing?zxid=%s" target="_blank">%s</a></td>' % (
        row[2], row[3])  # 会员信息
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'  # 订单状态 + 处理
        biaoge = biaoge + '<a href="/mem_zixun_liulan_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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
    return render(request, "pc/mem_zixun_liulan_list.html", context=neirong)


# 信息 详情
def xinxi_xiangqing(request):
    if request.method == "GET":
        zxid = request.GET.get("zxid")
        curson = connection.cursor()
        curson.execute("select * from xinwen where id=%s" % zxid)
        info = curson.fetchone()

        # 读取上一篇资讯
        shang = ""
        curson_shang = connection.cursor()
        curson_shang.execute("select id,xinxi_biaoti from xinwen where id<%s  order by id desc limit 0,1" % zxid)
        info_shang = curson_shang.fetchone()
        if info_shang:
            shang = "<a href=/xinxi_xiangqing?zxid=%s>%s</a>" % (info_shang[0], info_shang[1])
        else:
            shang = "暂无"
        # print(shang)

        # 读取下一篇资讯
        xia = ""
        curson_xia = connection.cursor()
        curson_xia.execute("select id,xinxi_biaoti from xinwen where id>%s  order by id asc limit 0,1" % zxid)
        info_xia = curson_xia.fetchone()
        if info_xia:
            xia = "<a href=/xinxi_xiangqing?zxid=%s>%s</a>" % (info_xia[0], info_xia[1])
        else:
            xia = "暂无"
        # print(xia)

        # 插入阅读记录
        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        h_id = request.COOKIES.get("h_id")
        if h_id is None:
            curson_insert = connection.cursor()
            sql_insert = "insert into xinwen_liulan(zixun_id,riqi,shijian) values ('%s','%s','%s')" % (
            zxid, add_riqi, add_shijian)
            curson_insert.execute(sql_insert)
        else:
            curson_insert = connection.cursor()
            sql_insert = "insert into xinwen_liulan(zixun_id,u_id,riqi,shijian) values ('%s','%s','%s','%s')" % (
            zxid, h_id, add_riqi, add_shijian)
            curson_insert.execute(sql_insert)

        # 读取 浏览阅读数
        shu_liulan = 0
        cursor_shu_liulan = connection.cursor()
        sql_shu_liulan = "select count(1) from xinwen_liulan where zixun_id=%s" % zxid
        cursor_shu_liulan.execute(sql_shu_liulan)
        shu_liulan = cursor_shu_liulan.fetchone()[0]

        # 读取 收藏数
        shu_shoucang = 0
        cursor_shu_shoucang = connection.cursor()
        sql_shu_shoucang = "select count(1) from xinwen_shoucang where zixun_id=%s" % zxid
        cursor_shu_shoucang.execute(sql_shu_shoucang)
        shu_shoucang = cursor_shu_shoucang.fetchone()[0]

        # 读取评论信息   状态yn_shenhe  0-等待审核  1-审核拒绝 2-审核通过
        curson_pinglun_list = connection.cursor()
        curson_pinglun_list.execute(
            "select id,neirong,riqi  from xinwen_pinglun where yn_shenhe=2 and zixun_id=%s" % zxid)
        rows_pinglun_list = curson_pinglun_list.fetchall()
        # print(rows_pinglun_list)

        # 读取评论数
        shu_pinglun = 0
        cursor_shu_pinglun = connection.cursor()
        sql_shu_pinglun = "select count(1) from xinwen_pinglun where zixun_id=%s" % zxid
        cursor_shu_pinglun.execute(sql_shu_pinglun)
        shu_pinglun = cursor_shu_pinglun.fetchone()[0]

        neirong = {
            "info": info,
            "zxid": zxid,
            "rows_pinglun_list": rows_pinglun_list,
            "shu_shoucang": shu_shoucang,
            "shu_pinglun": shu_pinglun,
            "shu_liulan": shu_liulan,
            "shang": shang,
            "xia": xia
        }
        return render(request, "pc/xinxi_xiangqing.html", context=neirong)


# 资讯信息 列表
def xinxi_list(request, dijiye, leixing_id):
    # print("第几页=%s" % dijiye)
    # print("当前信息类型id=%s" % leixing_id)

    chaxun = ""
    if request.GET.get("remen") is None:
        chaxun = ""
    else:
        chaxun = request.GET.get("remen")
    # print("查询关键字=%s" % chaxun)

    # 读取分类
    curson_fenlei = connection.cursor()
    curson_fenlei.execute("select id,caidan_mingcheng from xinwen_fenlei where caidan_jibie=1 ")
    fenleis_fenlei = curson_fenlei.fetchall()

    cursor_zongshuju = connection.cursor()
    sql_zongshuju = ""
    # sql_zongshuju = "select count(1) from xinwen"
    if leixing_id == "0":  # 字符串 非整数，后面要转
        if chaxun is None:
            sql_zongshuju = "select count(1) from xinwen"
        else:
            sql_zongshuju = "select count(1) from xinwen where xinxi_biaoti like '%" + chaxun + "%' "
    else:
        sql_zongshuju = "select count(1) from xinwen where   xinxi_lxid1=%s" % leixing_id

    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    # print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 8
    yeshu = math.ceil(zongshuju / meiye)
    # print("每页数据 =%s 条" % meiye)
    # print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    # sql = "select * from xinwen order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    if leixing_id == "0":  # 字符串 非整数，后面要转
        if chaxun is None:
            sql = "select * from xinwen order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
        else:
            sql = "select * from xinwen where xinxi_biaoti like '%%%s%%'  order by id desc limit %s,%s" % (
            chaxun, (int(meiye) * int(dijiye)), meiye)
    else:
        sql = "select * from xinwen where xinxi_lxid1=%s order by id desc limit %s,%s" % (
        leixing_id, int(meiye) * int(dijiye), meiye)

    # print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="99%" border="0" cellspacing="1" cellpadding="5" bgcolor="#F9F9F9">'
    for row in rows:
        tmp_leixing = ""

        tmp_tuijian = ""
        if row[5] == 1:
            tmp_tuijian = "有"

        tmp_tupian = ""
        if row[7] == 1:
            tmp_tupian = "有"

        curson = connection.cursor()
        curson.execute("select * from xinwen_fenlei where id=%s" % row[1])
        tmp_leixing = curson.fetchone()
        biaoge = biaoge + '<tr><td style="padding:7px;border-bottom: 1px dotted gainsboro;" height="35px;">'
        biaoge = biaoge + '<a  target="_blank" href="/xinxi_xiangqing?zxid=%s">' % row[0]
        biaoge = biaoge + '[%s] ' % row[11]
        biaoge = biaoge + '%s' % row[3]
        biaoge = biaoge + '</a>'
        biaoge = biaoge + '</td></tr>'

    biaoge = biaoge + '</table>'
    caidan = ""

    caidan = caidan + '<br><a href="/xinxi_list/0/%s?remen=%s">首页</a>&nbsp;&nbsp;' % (leixing_id, chaxun)
    if int(dijiye) >= 1:
        caidan = caidan + '<a href="/xinxi_list/%s/%s?remen=%s">上一页</a>&nbsp;&nbsp;' % (
        (int(dijiye) - 1), leixing_id, chaxun)
    else:
        caidan = caidan + '上一页&nbsp;&nbsp;'

    if int(dijiye) >= (int(yeshu) - 1):
        caidan = caidan + '下一页&nbsp;&nbsp;'
    else:
        caidan = caidan + '<a href="/xinxi_list/%s/%s?remen=%s">下一页</a>&nbsp;&nbsp;' % (
        (int(dijiye) + 1), leixing_id, chaxun)

    caidan = caidan + '<a href="/xinxi_list/%s/%s?remen=%s">尾页</a>&nbsp;&nbsp;' % ((int(yeshu) - 1), leixing_id, chaxun)

    caidan = caidan + "总数据：%s | " % zongshuju
    caidan = caidan + "每页：%s | " % meiye
    caidan = caidan + "当前页数：%s | " % (int(dijiye) + 1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "dijiye": dijiye,
        "leixing_id": int(leixing_id),
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge,
        "fenleis_fenlei": fenleis_fenlei,
        "chaxun": chaxun
    }
    return render(request, "pc/xinxi_list.html", context=neirong)
