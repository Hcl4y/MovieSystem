from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

import time
from datetime import datetime
from django.utils.timezone import make_aware
import json

import math
#热门关键字设定
def set_key_remen_xinwen(request):
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
        return render(request, "houtai/xinwen/set_key_remen_xinwen.html", context=neirong)
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
        return redirect("/set_key_remen_xinwen")

#分类录入和修改
def xiangmu_fenlei(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        row_edit = ""
        # 如果是修改，则读取要修改的内容
        if id_1ji:
            curson_edit = connection.cursor()
            sql_edit = "select * from xiangmu_fenlei where id=%s" % id_1ji
            curson_edit.execute(sql_edit)
            row_edit = curson_edit.fetchone()

        # 读取所有1级菜单
        curson = connection.cursor()
        curson.execute("select * from xiangmu_fenlei")
        rows = curson.fetchall()
        neirong = {
            "caidan_1jis": rows,
            "id_1ji": id_1ji,
            "caidan_info": row_edit
        }
        return render(request, "houtai/xiangmu/xiangmu_fenlei.html", context=neirong)

    if request.method == "POST":
        # 判断id_1ji，有值则是修改，没有则是新录入
        id_1ji = request.POST.get("id_1ji")
        if id_1ji:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "update xiangmu_fenlei set caidan_mingcheng='%s',paixu_id=%s where id=%s" % (
            caidan_mingcheng, paixu_id, id_1ji)
            curson.execute(sql)
        else:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "insert into xiangmu_fenlei(caidan_mingcheng,paixu_id) values ('%s',%s)" % (
                caidan_mingcheng, paixu_id)
            curson.execute(sql)
        return redirect("/xiangmu_fenlei")

#分类删除 表：0-id    1-caidan_mingcheng   2-paixu_id
def xiangmu_fenlei_del(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        print("删除分类id=%s" % id_1ji)
        curson = connection.cursor()
        sql = "delete from xiangmu_fenlei where id=%s" % id_1ji
        curson.execute(sql)
        return redirect("/xiangmu_fenlei")

#项目 电影 录入
def xiangmu_add(request):
    if request.method == "GET":
        curson = connection.cursor()
        curson.execute("select * from xiangmu_fenlei ")
        fenzus = curson.fetchall()
        neirong = {
            "fenzus": fenzus
        }
        return render(request, "houtai/xiangmu/xiangmu_add.html", context=neirong)

    if request.method == "POST":
        xinxi_lxid = request.POST.get("xinxi_lxid")    #类型
        xinxi_biaoti = request.POST.get("xinxi_biaoti")#标题
        jiage = request.POST.get("jiage")              #价格
        xinxi_riqi = request.POST.get("xinxi_riqi")    #日期
        #推荐简介
        xinxi_jianjie_yn = request.POST.get("jianjie_yn")
        if xinxi_jianjie_yn == "on":
            xinxi_jianjie_yn = 1
        else:
            xinxi_jianjie_yn = 0
        xinxi_jianjie = request.POST.get("xinxi_jianjie")
        #封面图片
        xinxi_tupian_yn = request.POST.get("tupian_yn")
        if xinxi_tupian_yn == "on":
            xinxi_tupian_yn = 1
        else:
            xinxi_tupian_yn = 0
        xinxi_tupian = request.POST.get("xinxi_tupian")

        xinxi_neirong = request.POST.get("xinxi_neirong")
        shichang = request.POST.get("shichang")  #时长

        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        curson = connection.cursor()
        sql = "insert into xiangmu(xinxi_lxid,xinxi_biaoti,jiage,xinxi_riqi,xinxi_jianjie_yn,xinxi_jianjie,xinxi_tupian_yn,xinxi_tupian,xinxi_neirong,add_riqi,add_shijian,shichang) " \
              "values (%s,'%s',%s,'%s',%s,'%s',%s,'%s','%s','%s','%s',%s)" \
              % (xinxi_lxid, xinxi_biaoti,jiage, xinxi_riqi, xinxi_jianjie_yn, xinxi_jianjie, xinxi_tupian_yn, xinxi_tupian,
                 xinxi_neirong, add_riqi, add_shijian,shichang)
        curson.execute(sql)
        return redirect("/xiangmu_list/0")

#项目 电影 修改
def xiangmu_xiugai(request):
    if request.method == "GET":
        curson_fenzu = connection.cursor()
        curson_fenzu.execute("select * from xiangmu_fenlei")
        fenzus = curson_fenzu.fetchall()

        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        curson.execute("select * from xiangmu where id=%s" % id)
        info = curson.fetchone()
        print(info[3])

        neirong = {
            "fenzus": fenzus,
            "info": info,
            "fzid": info[1],
            "dijiye":dijiye
        }
        return render(request, "houtai/xiangmu/xiangmu_xiugai.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")
        dijiye = request.POST.get("dijiye")

        xinxi_lxid = request.POST.get("xinxi_lxid")
        xinxi_biaoti = request.POST.get("xinxi_biaoti")
        jiage = request.POST.get("jiage")
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
        shichang = request.POST.get("shichang") #时长

        # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
        curson = connection.cursor()
        sql = "update xiangmu set xinxi_lxid=%s,xinxi_biaoti='%s',jiage=%s,xinxi_riqi='%s',xinxi_jianjie_yn=%s,xinxi_jianjie='%s'," \
              "xinxi_tupian_yn=%s,xinxi_tupian='%s',xinxi_neirong='%s',shichang=%s where id=%s" % \
              (xinxi_lxid, xinxi_biaoti,jiage, xinxi_riqi, xinxi_jianjie_yn, xinxi_jianjie, xinxi_tupian_yn, xinxi_tupian,xinxi_neirong,shichang,id)
        curson.execute(sql)
        return redirect("/xiangmu_list/%s" % dijiye)

#项目 电影 删除
def xiangmu_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from xiangmu where id=%s" % id
        curson.execute(sql)
        return redirect("/xiangmu_list/%s" % dijiye)

#项目 电影 列表
def xiangmu_list(request, dijiye):
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xiangmu"
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    # sql = "select * from kecheng"
    sql = "select * from xiangmu order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据
    # for row in rows:
    #    print(row)

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">上架</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">标题</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="10%">类型</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="30%">推荐</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">缩略图</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%">操作</td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        tmp_leixing = ""

        tmp_tuijian = ""
        if row[5] == 1:
            tmp_tuijian = "有"
            tmp_tuijian = row[6]
        print(tmp_tuijian)

        tmp_tupian = ""
        if row[7] == 1:
            tmp_tupian = "有"
            tmp_tupian = "<img src='/%s' height='80px'>" % row[8]

        curson = connection.cursor()
        curson.execute("select * from xiangmu_fenlei where id=%s" % row[1])
        tmp_leixing = curson.fetchone()

        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % row[4]

        biaoge = biaoge + '<td bgcolor="#FFFFFF">' +row[2]
        biaoge = biaoge + "<a href='/xiangmu_mulu?xiangmu_id="+str(row[0])+"&xiangmu_mc="+row[2]+"'>【日期和场次安排】</a>"
        biaoge = biaoge + "<br>价格：" + str(row[3]) + " 元"
        biaoge = biaoge + "<br>时长：" + str(row[12]) + " 分钟"
        biaoge = biaoge + '</td>'

        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % tmp_leixing[1]
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % tmp_tuijian
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % tmp_tupian
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        biaoge = biaoge + '<a href="/xiangmu_xiugai?id=%s&dijiye=%s">修改</a>&nbsp;&nbsp;' % (row[0], dijiye)
        biaoge = biaoge + '| &nbsp;&nbsp;<a href="/xiangmu_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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

    return render(request, "houtai/xiangmu/xiangmu_list.html", context=neirong)

#项目 电影 目录
def xiangmu_mulu(request):
    if request.method == "GET":
        xiangmu_id = request.GET.get("xiangmu_id")
        xiangmu_mc = request.GET.get("xiangmu_mc")
        print("id=%s，名称=%s" % (xiangmu_id,xiangmu_mc))

        #读取该本书的1级目录
        curson_mulu1 = connection.cursor()
        curson_mulu1.execute("select  id,xinxi_biaoti,up_id  from xiangmu_mulu where mulu_jibie=1 and xiangmu_id=%s" %xiangmu_id )
        rows_mulu1 = curson_mulu1.fetchall()

        #读取该本书的2级目录
        curson_mulu2 = connection.cursor()
        curson_mulu2.execute("select  id,xinxi_biaoti,up_id  from xiangmu_mulu where mulu_jibie=2 and xiangmu_id=%s" %xiangmu_id )
        rows_mulu2 = curson_mulu2.fetchall()

        biaoge = ""

        neirong = {
            "rows_mulu1": rows_mulu1,
            "rows_mulu2": rows_mulu2,
            "xiangmu_id":xiangmu_id,
            "xiangmu_mc":xiangmu_mc,
        }
        return render(request, "houtai/xiangmu/xiangmu_mulu.html", context=neirong)

#项目 电影 日期安排 录入
def mulu1_add(request):
    if request.method == "GET":
        xiangmu_id = request.GET.get("xiangmu_id")  #
        xiangmu_mc = request.GET.get("xiangmu_mc")  #
        neirong = {
            "xiangmu_id": xiangmu_id,
            "xiangmu_mc": xiangmu_mc,
        }
        return render(request, "houtai/xiangmu/mulu1_add.html", context=neirong)

    if request.method == "POST":
        xiangmu_id = request.POST.get("xiangmu_id")  #
        xiangmu_mc = request.POST.get("xiangmu_mc")  #
        xinxi_biaoti = request.POST.get("xinxi_biaoti")#标题
        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        curson = connection.cursor()
        sql = "insert into xiangmu_mulu(xinxi_biaoti,add_riqi,add_shijian,xiangmu_id,xiangmu_mc,mulu_jibie) " \
              "values ('%s','%s','%s',%s,'%s',%s)" \
              % (xinxi_biaoti, add_riqi, add_shijian,xiangmu_id,xiangmu_mc,1)
        curson.execute(sql)
        return redirect("/xiangmu_mulu?xiangmu_id=%s&xiangmu_mc=%s" % (xiangmu_id,xiangmu_mc))

#项目 电影 日期安排 修改
def mulu1_xiugai(request):
    if request.method == "GET":
        id = request.GET.get("id")
        xiangmu_id = request.GET.get("xiangmu_id")
        xiangmu_mc = request.GET.get("xiangmu_mc")

        curson = connection.cursor()
        curson.execute("select * from xiangmu_mulu where id=%s" % id)
        info = curson.fetchone()
        print(info[3])

        neirong = {
            "xiangmu_id": xiangmu_id,
            "xiangmu_mc": xiangmu_mc,
            "info":info,
        }
        return render(request, "houtai/xiangmu/mulu1_xiugai.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")
        xiangmu_id = request.POST.get("xiangmu_id")  #
        xiangmu_mc = request.POST.get("xiangmu_mc")  #

        xinxi_biaoti = request.POST.get("xinxi_biaoti")#标题

        curson = connection.cursor()
        sql = "update xiangmu_mulu set xinxi_biaoti='%s'  where xiangmu_id=%s and id=%s" % \
              (xinxi_biaoti, xiangmu_id,id)
        curson.execute(sql)
        return redirect("/xiangmu_mulu?xiangmu_id=%s&xiangmu_mc=%s" % (xiangmu_id, xiangmu_mc))

#项目 电影 日期排期和场次 删除
def mulu_del(request):
    if request.method == "GET":
        id = request.GET.get("id")
        xiangmu_id = request.GET.get("xiangmu_id")
        xiangmu_mc = request.GET.get("xiangmu_mc")

        curson = connection.cursor()
        sql = "delete from xiangmu_mulu where xiangmu_id=%s and id=%s" % (xiangmu_id,id)
        curson.execute(sql)
        return redirect("/xiangmu_mulu?xiangmu_id=%s&xiangmu_mc=%s" % (xiangmu_id, xiangmu_mc))

#项目 电影 日期下的场次 录入
def mulu2_add(request):
    if request.method == "GET":
        xiangmu_id = request.GET.get("xiangmu_id")
        xiangmu_mc = request.GET.get("xiangmu_mc")
        up_id = request.GET.get("up_id")
        up_mc = request.GET.get("up_mc")

        neirong = {
            "xiangmu_id": xiangmu_id,
            "xiangmu_mc": xiangmu_mc,
            "up_id": up_id,
            "up_mc": up_mc,
        }
        return render(request, "houtai/xiangmu/mulu2_add.html", context=neirong)

    if request.method == "POST":
        xiangmu_id = request.POST.get("xiangmu_id")
        xiangmu_mc = request.POST.get("xiangmu_mc")
        up_id = request.POST.get("up_id")
        up_mc = request.POST.get("up_mc")

        xinxi_biaoti = request.POST.get("xinxi_biaoti") #标题

        yingting = request.POST.get("yingting")
        meipai = request.POST.get("meipai")
        jihang = request.POST.get("jihang")
        zongshu = int(meipai) * int(jihang)

        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        curson = connection.cursor()
        sql = "insert into xiangmu_mulu(xinxi_biaoti,add_riqi,add_shijian,xiangmu_id,xiangmu_mc,mulu_jibie,up_id,up_mc,yingting,meipai,jihang,zongshu) " \
              "values ('%s','%s','%s',%s,'%s',%s,%s,'%s',%s,%s,%s,%s)" \
              % (xinxi_biaoti,add_riqi,add_shijian,xiangmu_id,xiangmu_mc,2,up_id,up_mc,yingting,meipai,jihang,zongshu)
        curson.execute(sql)
        return redirect("/xiangmu_mulu?xiangmu_id=%s&xiangmu_mc=%s" % (xiangmu_id,xiangmu_mc))

#项目 影 日期下的场次 修改
def mulu2_xiugai(request):
    if request.method == "GET":
        id = request.GET.get("id")
        xiangmu_id = request.GET.get("xiangmu_id")
        xiangmu_mc = request.GET.get("xiangmu_mc")

        curson = connection.cursor()
        curson.execute("select * from xiangmu_mulu where id=%s" % id)
        info = curson.fetchone()
        print(info[3])

        neirong = {
            "xiangmu_id": xiangmu_id,
            "xiangmu_mc": xiangmu_mc,
            "info":info,
        }
        return render(request, "houtai/xiangmu/mulu2_xiugai.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")
        xiangmu_id = request.POST.get("xiangmu_id")  #
        xiangmu_mc = request.POST.get("xiangmu_mc")  #

        xinxi_biaoti = request.POST.get("xinxi_biaoti") #标题

        yingting = request.POST.get("yingting")
        meipai = request.POST.get("meipai")
        jihang = request.POST.get("jihang")
        zongshu = int(meipai) * int(jihang)

        curson = connection.cursor()
        sql = "update xiangmu_mulu set xinxi_biaoti='%s',yingting=%s,meipai=%s,jihang=%s,zongshu=%s  where xiangmu_id=%s and id=%s" % \
              (xinxi_biaoti,yingting,meipai,jihang,zongshu, xiangmu_id,id)
        curson.execute(sql)
        return redirect("/xiangmu_mulu?xiangmu_id=%s&xiangmu_mc=%s" % (xiangmu_id, xiangmu_mc))


####################################################################################################################
#订单列表
def xiangmu_dingdan_list(request, dijiye):
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xiangmu_dingdan"
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select * from xiangmu_dingdan order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="12%">会员</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="13%">电影名称</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%" height="30">预约日期|场次</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%">座位信息</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">费用信息</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%">状态</td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        huiyuan = ""
        curson_huiyuan = connection.cursor()
        curson_huiyuan.execute("select * from huiyuan where id=%s" % row[1])
        tmp_huiyuan = curson_huiyuan.fetchone()
        huiyuan = huiyuan + tmp_huiyuan[1]

        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' % huiyuan  # 会员信息
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/pc_dianzishu_xiangqing?id=%s" target="_blank">%s</a></td>' % ( row[2], row[3])
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="50">预约日期：%s<br>预约场次：%s</td>' %  (row[4],row[6] )
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        biaoge = biaoge + row[8]
        biaoge = biaoge + '</td>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        biaoge = biaoge + '费用：%s 元 <br>票数：%s 张' %(row[10],row[9])
        biaoge = biaoge + '</td>'

        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        if row[13] == 1 :
            biaoge = biaoge + '待支付'
            biaoge = biaoge + '&nbsp;&nbsp;&nbsp;&nbsp;<a href="/api_dianying_dingdan_del?id=%s&dijiye=%s">取消订单</a>' % (row[0], dijiye)
        if row[13] == 2 :
            biaoge = biaoge + '已付款'
        biaoge = biaoge + '</td>'
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
    caidan = caidan + "当前页数：%s | " % (int(dijiye)+1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge
    }

    return render(request, "houtai/xiangmu/xiangmu_dingdan_list.html", context=neirong)

#订单删除
def xiangmu_dingdan_del(request):
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")

        curson = connection.cursor()
        sql = "delete from xiangmu_dingdan where id=%s" % id
        curson.execute(sql)
        return redirect("/xiangmu_dingdan_list/%s" % dijiye)

#评论列表
def xiangmu_pinglun_list(request, dijiye):
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xiangmu_pinglun"
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select * from xiangmu_pinglun order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
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
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' %  row[5] #评论时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' %  huiyuan #会员信息
        biaoge = biaoge + '<td bgcolor="#FFFFFF">%s</td>' %  row[3]  #内容


        biaoge = biaoge + '<td bgcolor="#FFFFFF">' #状态 + 处理
        #状态：0待处理，1拒绝，2通过
        if row[6]==0:
            biaoge = biaoge + "0-等待审核 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            biaoge = biaoge + '<a href="/xiangmu_pinglun_chuli?id=%s&dijiye=%s">评论处理</a>' % (row[0], dijiye)
        if row[6]==1:
            biaoge = biaoge + "1-审核拒绝 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            biaoge = biaoge + '<a href="/xiangmu_pinglun_chuli?id=%s&dijiye=%s">评论处理</a>' % (row[0], dijiye)
        if row[6]==2:
            biaoge = biaoge + "2-审核通过 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            biaoge = biaoge + '<a href="/xiangmu_pinglun_chuli?id=%s&dijiye=%s">评论处理</a>' % (row[0], dijiye)

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
    caidan = caidan + "当前页数：%s | " % (int(dijiye)+1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge
    }

    return render(request, "houtai/xiangmu/xiangmu_pinglun_list.html", context=neirong)

#评论处理
def xiangmu_pinglun_chuli(request):
    if request.method == "GET":

        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        curson.execute("select * from xiangmu_pinglun where id=%s" % id)
        info = curson.fetchone()

        neirong = {
            "id":id,
            "dijiye":dijiye,
            "yn_shenhe": info[6],
            "shenhe_beizhu": info[7]
        }
        return render(request, "houtai/xiangmu/xiangmu_pinglun_chuli.html", context=neirong)

    if request.method == "POST":
        id = request.POST.get("id")
        dijiye = request.POST.get("dijiye")

        yn_shenhe = request.POST.get("yn_shenhe")
        shenhe_beizhu = request.POST.get("shenhe_beizhu")

        curson = connection.cursor()
        sql = "update xiangmu_pinglun set yn_shenhe=%s,shenhe_beizhu='%s' where id=%s" % \
              (yn_shenhe, shenhe_beizhu,id)
        curson.execute(sql)
        return redirect("/xiangmu_pinglun_list/%s" % dijiye)