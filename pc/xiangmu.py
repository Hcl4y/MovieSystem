import math

from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse

from datetime import  datetime
from django.utils.timezone import make_aware
import json
import time

#顶部查询
def chaxun(request):
    print(request.POST.get("chaxun_neirong"))
    chaxun_neirong = request.POST.get("chaxun_neirong")
    if chaxun_neirong is None:
        myurl = "/pc_xiangmu_list/0/0"
    else:
        myurl = "/pc_xiangmu_list/0/0?remen=" + chaxun_neirong
    print(myurl)
    return redirect( myurl )

#项目 电影 列表
def pc_xiangmu_list(request,dijiye,leixing_id):
    print("第几页=%s" % dijiye)
    print("当前信息类型id=%s" % leixing_id)


    chaxun = ""
    if request.GET.get("remen") is None:
        chaxun=""
    else:
        chaxun = request.GET.get("remen")
    print("查询关键字=%s" % chaxun)

    #读取分类
    curson_fenlei = connection.cursor()
    curson_fenlei.execute("select id,caidan_mingcheng from xiangmu_fenlei")
    fenleis_fenlei = curson_fenlei.fetchall()


    cursor_zongshuju = connection.cursor()
    sql_zongshuju = ""
    #sql_zongshuju = "select count(1) from xinwen"
    if leixing_id=="0": #字符串 非整数，后面要转
        if chaxun is None:
            sql_zongshuju = "select count(1) from xiangmu"
        else:
            sql_zongshuju = "select count(1) from xiangmu where xinxi_biaoti like '%"+chaxun+"%' "
    else:
        sql_zongshuju = "select count(1) from xiangmu where   xinxi_lxid=%s" % leixing_id

    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)
    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    #sql = "select * from xinwen order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
    if leixing_id == "0":  # 字符串 非整数，后面要转
        if chaxun is None:
            sql = "select * from xiangmu order by id desc limit %s,%s" % (int(meiye) * int(dijiye), meiye)
        else:
            sql = "select * from xiangmu where xinxi_biaoti like '%%%s%%'  order by id desc limit %s,%s" % (chaxun,(int(meiye) * int(dijiye)), meiye)
    else:
        sql = "select * from xiangmu where xinxi_lxid=%s order by id desc limit %s,%s" % (leixing_id, int(meiye) * int(dijiye), meiye)

    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="99%" border="0" cellspacing="1" cellpadding="5" bgcolor="#F9F9F9">'
    for row in rows:
        tmp_leixing = ""

        tmp_tuijian = ""
        if row[5] == 1:
            tmp_tuijian = "有"

        tmp_tupian =""
        if  row[7] == 1:
            tmp_tupian = "有"

        # curson = connection.cursor()
        # curson.execute("select * from cp_leixing where id=%s" % row[1])
        # tmp_leixing = curson.fetchone()

        biaoge = biaoge + '<tr><td style="padding:7px;border-bottom: 1px dotted gainsboro;">'
        biaoge = biaoge + '<a  target="_blank" href="/pc_xiangmu_xiangqing?id=%s">' % row[0]
        biaoge = biaoge + '<table width="100%" border="0" cellspacing="0" cellpadding="0">'
        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '    <td rowspan="3" width="150px" align="center"><img src="http://%s/%s" height="88px"></td>' % (request.get_host(),row[8])
        biaoge = biaoge + '    <td>电影标题：%s（价格：%s 元）</td>' % (row[2],row[3])
        biaoge = biaoge + '  </tr>'
        biaoge = biaoge + '  <tr>'
        biaoge = biaoge + '    <td style="color:#999;">上架日期：%s</td>' % row[4]
        biaoge = biaoge + '  </tr>'
        biaoge = biaoge + '  <tr>'
        biaoge = biaoge + '    <td style="color:#999;">简介推荐：%s</td>' % row[6]
        biaoge = biaoge + '  </tr>'
        biaoge = biaoge + '</table>'
        biaoge = biaoge + '</a>'
        biaoge = biaoge + '<td></tr>'

    biaoge = biaoge + '</table>'
    caidan = ""

    caidan = caidan + '<br><a href="/pc_xiangmu_list/0/%s?remen=%s">首页</a>&nbsp;&nbsp;' % (leixing_id,chaxun)
    if int(dijiye) >= 1:
        caidan = caidan + '<a href="/pc_xiangmu_list/%s/%s?remen=%s">上一页</a>&nbsp;&nbsp;' % ((int(dijiye) - 1),leixing_id,chaxun)
    else:
        caidan = caidan + '上一页&nbsp;&nbsp;'

    if int(dijiye) >= (int(yeshu) - 1):
        caidan = caidan + '下一页&nbsp;&nbsp;'
    else:
        caidan = caidan + '<a href="/pc_xiangmu_list/%s/%s?remen=%s">下一页</a>&nbsp;&nbsp;' % ((int(dijiye) + 1),leixing_id,chaxun)

    caidan = caidan + '<a href="/pc_xiangmu_list/%s/%s?remen=%s">尾页</a>&nbsp;&nbsp;' % ((int(yeshu) - 1),leixing_id,chaxun)

    caidan = caidan + "总数据：%s | " % zongshuju
    caidan = caidan + "每页：%s | " % meiye
    caidan = caidan + "当前页数：%s | " % (int(dijiye)+1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "dijiye": dijiye,
        "leixing_id": int(leixing_id),
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge,
        "fenleis_fenlei":fenleis_fenlei,
        "chaxun":chaxun
    }
    return render(request, "pc/pc_xiangmu_list.html", context=neirong)

#项目 电影 详情
def pc_xiangmu_xiangqing(request):
    if request.method == "GET":
        cpid = request.GET.get("id")
        curson = connection.cursor()
        curson.execute("select * from xiangmu where id=%s" % cpid)
        info = curson.fetchone()

        h_id = request.COOKIES.get("h_id")  # 登录的用户id

        #读取1级目录
        curson_mulu1 = connection.cursor()
        curson_mulu1.execute("select  id,xinxi_biaoti,up_id  from xiangmu_mulu where mulu_jibie=1 and xiangmu_id=%s" %cpid )
        rows_mulu1 = curson_mulu1.fetchall()

        #读取2级目录
        curson_mulu2 = connection.cursor()
        curson_mulu2.execute("select  id,xinxi_biaoti,up_id  from xiangmu_mulu where mulu_jibie=2 and xiangmu_id=%s" %cpid )
        rows_mulu2 = curson_mulu2.fetchall()

        #读取上一个
        shang =""
        curson_shang = connection.cursor()
        curson_shang.execute("select id,xinxi_biaoti from xiangmu where id<%s  order by id desc limit 0,1" % cpid)
        info_shang = curson_shang.fetchone()
        if info_shang:
            shang = "<a href=/pc_xiangmu_xiangqing?id=%s>%s</a>" %(info_shang[0],info_shang[1])
        else:
            shang = "暂无"
        print(shang)

        #读取下一个
        xia =""
        curson_xia = connection.cursor()
        curson_xia.execute("select id,xinxi_biaoti from xiangmu where id>%s  order by id asc limit 0,1" % cpid)
        info_xia = curson_xia.fetchone()
        if info_xia:
            xia = "<a href=/pc_xiangmu_xiangqing?id=%s>%s</a>" %(info_xia[0],info_xia[1])
        else:
            xia = "暂无"
        print(xia)

        #插入阅读记录
        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        h_id = request.COOKIES.get("h_id")
        if h_id is None:
            curson_insert = connection.cursor()
            sql_insert = "insert into xiangmu_liulan(xiangmu_id,riqi,shijian) values ('%s','%s','%s')" % (cpid, add_riqi, add_shijian)
            curson_insert.execute(sql_insert)
        else:
            curson_insert = connection.cursor()
            sql_insert = "insert into xiangmu_liulan(xiangmu_id,u_id,riqi,shijian) values ('%s','%s','%s','%s')" % (cpid, h_id, add_riqi, add_shijian)
            curson_insert.execute(sql_insert)

        #读取 浏览阅读数
        shu_liulan = 0
        cursor_shu_liulan = connection.cursor()
        sql_shu_liulan = "select count(1) from xiangmu_liulan where xiangmu_id=%s" % cpid
        cursor_shu_liulan.execute(sql_shu_liulan)
        shu_liulan = cursor_shu_liulan.fetchone()[0]

        #读取 收藏数
        shu_shoucang = 0
        cursor_shu_shoucang = connection.cursor()
        sql_shu_shoucang = "select count(1) from xiangmu_shoucang where xiangmu_id=%s" % cpid
        cursor_shu_shoucang.execute(sql_shu_shoucang)
        shu_shoucang = cursor_shu_shoucang.fetchone()[0]

        # 读取评论信息   状态yn_shenhe  0-等待审核  1-审核拒绝 2-审核通过
        curson_pinglun_list = connection.cursor()
        curson_pinglun_list.execute("select id,neirong,riqi  from xiangmu_pinglun where yn_shenhe=2 and xiangmu_id=%s" % cpid)
        rows_pinglun_list = curson_pinglun_list.fetchall()
        print(rows_pinglun_list)

        #读取评论数
        shu_pinglun = 0
        cursor_shu_pinglun = connection.cursor()
        sql_shu_pinglun = "select count(1) from xiangmu_pinglun where xiangmu_id=%s" % cpid
        cursor_shu_pinglun.execute(sql_shu_pinglun)
        shu_pinglun = cursor_shu_pinglun.fetchone()[0]

        neirong = {
            "info": info,
            "rows_mulu1": rows_mulu1,
            "rows_mulu2": rows_mulu2,
            "yn_goumai":1,
            "cpid":cpid,
            "rows_pinglun_list":rows_pinglun_list,
            "shu_shoucang":shu_shoucang,
            "shu_pinglun":shu_pinglun,
            "shu_liulan":shu_liulan,
            "shang":shang,
            "xia": xia
        }
        return render(request, "pc/pc_xiangmu_xiangqing.html", context=neirong)

#项目 电影票 选座购买界面
def pc_xiangmu_ding(request):
    if request.method == "GET":
        xiangmu_id = request.GET.get("xiangmu_id")
        curson = connection.cursor()
        curson.execute("select * from xiangmu where id=%s" % xiangmu_id)
        info = curson.fetchone()

        h_id = request.COOKIES.get("h_id")  # 登录的用户id

        #读取电影排期-日期
        curson_mulu1 = connection.cursor()
        curson_mulu1.execute("select  id,xinxi_biaoti,up_id  from xiangmu_mulu where mulu_jibie=1 and xiangmu_id=%s" %xiangmu_id )
        rows_mulu1 = curson_mulu1.fetchall()

        #读取电影排期-日期-下的场次
        curson_mulu2 = connection.cursor()
        curson_mulu2.execute("select  id,xinxi_biaoti,up_id  from xiangmu_mulu where mulu_jibie=2 and xiangmu_id=%s" %xiangmu_id )
        rows_mulu2 = curson_mulu2.fetchall()

        #获取是否有场次信息，有场次信息则显示对应座位信息
        changci_id = request.GET.get("changci_id")

        zuoweis_yigou = "" #已经订购的座位集合

        info_changci = ""
        if changci_id:
            print("当前场次id=%s" % changci_id)
            #读取对应场次信息
            curson_changci = connection.cursor()
            curson_changci.execute("select * from xiangmu_mulu where id=%s" % changci_id)
            info_changci = curson_changci.fetchone()
            #读取该场次已经被预订的座位信息，集合

            cursor_yigou = connection.cursor()
            sql_yigou = "select * from xiangmu_dingdan where yuyue_changciid=%s" % changci_id
            cursor_yigou.execute(sql_yigou)
            rows = cursor_yigou.fetchall()  # 获取所有的数据
            for row in rows:
                zuoweis_yigou = zuoweis_yigou + row[8] + ","

        else:
            changci_id = 0

        neirong = {
            "info": info,
            "rows_mulu1": rows_mulu1,
            "rows_mulu2": rows_mulu2,
            "xiangmu_id":xiangmu_id,
            "info_changci":info_changci,
            "h_id":h_id,
            "changci_id":int(changci_id),
            "zuoweis_yigou":zuoweis_yigou
        }
        return render(request, "pc/pc_xiangmu_ding.html", context=neirong)

#项目 电影票 提交订单
def api_xiangmu_ding_add(request):
    u_id = request.GET.get("u_id")
    xiangmu_id = request.GET.get("xiangmu_id")
    xiangmu_mc = request.GET.get("xiangmu_mc")
    jiage = request.GET.get("jiage")

    yuyue_riqi = request.GET.get("yuyue_riqi")
    yuyue_riqiid = request.GET.get("yuyue_riqiid")

    yuyue_changci = request.GET.get("yuyue_changci")
    yuyue_changciid = request.GET.get("yuyue_changciid")

    yuyue_zuoweis = request.GET.get("yuyue_zuoweis")
    yuyue_piaoshu = request.GET.get("yuyue_piaoshu")
    yuyue_feiyong = request.GET.get("yuyue_feiyong")

    riqi = time.strftime("%Y-%m-%d", time.localtime())
    shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 写入数据库
    curson_insert = connection.cursor()
    sql_insert = "insert into xiangmu_dingdan(u_id,xiangmu_id,xiangmu_mc,yuyue_riqi,yuyue_riqiid,yuyue_changci,yuyue_changciid,yuyue_zuoweis,yuyue_piaoshu,yuyue_feiyong,riqi,shijian,zt)" \
                 "  values (%s,%s,'%s','%s',%s,'%s',%s,'%s',%s,%s,'%s','%s',1)"  \
                 % (u_id,xiangmu_id,xiangmu_mc,yuyue_riqi,yuyue_riqiid,yuyue_changci,yuyue_changciid,yuyue_zuoweis,yuyue_piaoshu,yuyue_feiyong,riqi,shijian)
    curson_insert.execute(sql_insert)
    cuowu = "<script>alert('电影票订单提交成功！');window.parent.location='/pc_xiangmu_xiangqing?id="+xiangmu_id+"';</script>"

    return  HttpResponse(cuowu)

#电影 收藏
def api_xiangmu_shoucang(request):
    xiangmu_id = request.GET.get("cpid")
    u_id = request.GET.get("h_id")
    mc = request.GET.get("mc")
    print("要收藏的id=%s,用户id=%s" %(xiangmu_id,u_id))

    #判断是否购买，如果没有购买，则写入数据库
    curson = connection.cursor()
    curson.execute("select * from xiangmu_shoucang where xiangmu_id='%s' and u_id='%s' " % (xiangmu_id,u_id))
    info = curson.fetchone()
    cuowu = ""
    if info:
        cuowu = "<script>alert('已经收藏')</script>"
    else:
        # #写入数据库
        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        curson_insert = connection.cursor()
        sql_insert = "insert into xiangmu_shoucang(u_id,xiangmu_id,xiangmu_mc,riqi,shijian) values (%s,%s,'%s','%s','%s')"  % (u_id,xiangmu_id,mc,add_riqi,add_shijian)
        curson_insert.execute(sql_insert)
        cuowu = "<script>alert('收藏成功');</script>"
    return  HttpResponse(cuowu)

#电影 评论
def api_xiangmu_pinglun_add(request):
    xiangmu_id = request.GET.get("cpid") #商品id
    u_id = request.GET.get("h_id") #会员id
    neirong = request.GET.get("neirong") #评论内容

    # 判断是否评论，如果没有，则写入数据库
    curson = connection.cursor()
    curson.execute("select * from xiangmu_pinglun where u_id=%s and xiangmu_id=%s " % (u_id, xiangmu_id))
    info = curson.fetchone()
    cuowu = ""
    if info:
        cuowu = "<script>alert('您已经提交过评论');window.parent.location='/pc_xiangmu_xiangqing?id=" + str(xiangmu_id) + "';</script>"
    else:
        # #写入数据库
        add_riqi = time.strftime("%Y-%m-%d", time.localtime())
        add_shijian = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        curson_insert = connection.cursor()
        sql_insert = "insert into xiangmu_pinglun(neirong,u_id,xiangmu_id,riqi,shijian) values ('%s',%s,%s,'%s','%s')" % (neirong, u_id, xiangmu_id,add_riqi, add_shijian)
        curson_insert.execute(sql_insert)
        #cuowu = "<script>alert('您的评论已经提交，审核后显示！')</script>"
        cuowu = "<script>alert('您的评论已经提交，审核后显示！');window.parent.location='/pc_xiangmu_xiangqing?id=" + str(xiangmu_id) + "';</script>"
    return HttpResponse(cuowu)

#会员 电影 订单 列表
def mem_xiangmu_dingdan_list(request, dijiye):
    h_id = request.COOKIES.get("h_id")  # 登录的用户id
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xiangmu_dingdan where u_id=%s" % h_id
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select * from xiangmu_dingdan " \
          "where u_id=%s  order by  id desc limit %s,%s" % (h_id,int(meiye) * int(dijiye), meiye)
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()  # 获取所有的数据

    biaoge = ''
    biaoge = biaoge + '<table width="100%" border="0" cellspacing="1" cellpadding="5"  align="center" bgcolor="#F6F6F6">'
    biaoge = biaoge + '<tr>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">电影名称</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="25%" height="30">预约日期|场次</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="25%">座位信息</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="15%">费用信息</td>'
    biaoge = biaoge + '<td bgcolor="#E0F3FF"  width="20%">状态</td>'
    biaoge = biaoge + '</tr>'

    for row in rows:
        biaoge = biaoge + '<tr>'
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/pc_xiangmu_xiangqing?id=%s" target="_blank">%s</a></td>' % ( row[2], row[3])
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
            biaoge = biaoge + '&nbsp;&nbsp;&nbsp;&nbsp;<a href="/api_xiangmu_dingdan_fukuan?id=%s&dijiye=%s">立即付款</a>' % (row[0], dijiye)
            biaoge = biaoge + '&nbsp;&nbsp;&nbsp;&nbsp;<a href="/api_xiangmu_dingdan_del?id=%s&dijiye=%s">取消订单</a>' % (row[0], dijiye)
        if row[13] == 2 :
            biaoge = biaoge + '已付款'
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
    caidan = caidan + "当前页数：%s | " % (int(dijiye)+1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge
    }
    return render(request, "pc/mem_xiangmu_dingdan_list.html", context=neirong)

#会员 电影 订单 删除
def api_xiangmu_dingdan_del(request):
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")

        curson = connection.cursor()
        sql = "delete from xiangmu_dingdan where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_xiangmu_dingdan_list/%s" % dijiye)

#会员 电影 订单 模拟付款
def api_xiangmu_dingdan_fukuan(request):
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")

        curson = connection.cursor()
        sql = "update xiangmu_dingdan set zt=2  where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_xiangmu_dingdan_list/%s" % dijiye)

#会员 电影 收藏 列表
def mem_xiangmu_shoucang_list(request, dijiye):
    h_id = request.COOKIES.get("h_id")  # 登录的用户id
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xiangmu_shoucang where u_id=%s" % h_id
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select * from xiangmu_shoucang  " \
          "where u_id=%s  order by  id desc limit %s,%s" % (h_id,int(meiye) * int(dijiye), meiye)
    print(sql)
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
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' %  row[4] #时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/pc_xiangmu_xiangqing?id=%s" target="_blank">%s</a></td>' % ( row[2], row[3]) #会员信息
        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        biaoge = biaoge + '<a href="/mem_xiangmu_shoucang_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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
    caidan = caidan + "当前页数：%s | " % (int(dijiye)+1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge
    }
    return render(request, "pc/mem_xiangmu_shoucang_list.html", context=neirong)

#会员 电影 收藏 删除
def mem_xiangmu_shoucang_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")

        curson = connection.cursor()
        sql = "delete from xiangmu_shoucang where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_xiangmu_shoucang_list/%s" % dijiye)

#会员 电影 评论 列表
def mem_xiangmu_pinglun_list(request, dijiye):
    h_id = request.COOKIES.get("h_id")  # 登录的用户id
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xiangmu_pinglun where u_id=%s" % h_id
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select  pinglun.id as plid,pinglun.riqi,pinglun.neirong,pinglun.yn_shenhe,xm.id as xmid,xm.xinxi_biaoti from xiangmu_pinglun as pinglun,xiangmu as xm " \
          "where pinglun.xiangmu_id=xm.id and pinglun.u_id=%s  order by pinglun.id desc limit %s,%s" % (h_id,int(meiye) * int(dijiye), meiye)
    print(sql)
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
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' %  row[1] #时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/pc_xiangmu_xiangqing?id=%s" target="_blank">%s</a></td>' % ( row[4], row[5])
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' % row[2]  # 评论时间

        biaoge = biaoge + '<td bgcolor="#FFFFFF">' #订单状态 + 处理
        if row[3]==0:
            biaoge = biaoge + '状态：待审核'
        if row[3]==1:
            biaoge = biaoge + '状态：拒绝'
        if row[3]==2:
            biaoge = biaoge + '状态：已通过'
        biaoge = biaoge + '</td>'

        biaoge = biaoge + '<td bgcolor="#FFFFFF">'
        if row[3]==0:
            biaoge = biaoge + '<a href="/mem_xiangmu_pinglun_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
        if row[3]==1:
            biaoge = biaoge + '<a href="/mem_xiangmu_pinglun_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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
    caidan = caidan + "当前页数：%s | " % (int(dijiye)+1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge
    }
    return render(request, "pc/mem_xiangmu_pinglun_list.html", context=neirong)

#会员 电影 评论 删除
def mem_xiangmu_pinglun_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from xiangmu_pinglun where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_xiangmu_pinglun_list/%s" % dijiye)

#会员 电影 浏览 列表
def mem_xiangmu_liulan_list(request, dijiye):
    h_id = request.COOKIES.get("h_id")  # 登录的用户id
    print("第几页=%s" % dijiye)
    cursor_zongshuju = connection.cursor()
    sql_zongshuju = "select count(1) from xiangmu_liulan where u_id=%s" % h_id
    cursor_zongshuju.execute(sql_zongshuju)
    zongshuju = cursor_zongshuju.fetchone()[0]
    print("总的数据= %s 条" % zongshuju)  # 12

    meiye = 5
    yeshu = math.ceil(zongshuju / meiye)

    print("每页数据 =%s 条" % meiye)
    print("有多少页 =%s " % yeshu)

    cursor = connection.cursor()
    sql = "select  liulan.id as llid,liulan.riqi,xm.id as xmid,xm.xinxi_biaoti from xiangmu_liulan as liulan,xiangmu as xm " \
          "where liulan.xiangmu_id=xm.id and liulan.u_id=%s  order by liulan.id desc limit %s,%s" % (h_id,int(meiye) * int(dijiye), meiye)
    print(sql)
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
        biaoge = biaoge + '<td bgcolor="#FFFFFF" height="27">%s</td>' %  row[1] #时间
        biaoge = biaoge + '<td bgcolor="#FFFFFF"><a href="/pc_xiangmu_xiangqing?id=%s" target="_blank">%s</a></td>' % ( row[2], row[3])
        biaoge = biaoge + '<td bgcolor="#FFFFFF">' #订单状态 + 处理
        biaoge = biaoge + '<a href="/mem_xiangmu_liulan_del?id=%s&dijiye=%s">删除</a>' % (row[0], dijiye)
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
    caidan = caidan + "当前页数：%s | " % (int(dijiye)+1)
    caidan = caidan + "总页数：%s  " % yeshu
    caidan = caidan + ""

    neirong = {
        "rows": rows,
        "caidan": caidan,
        "biaoge": biaoge
    }
    return render(request, "pc/mem_xiangmu_liulan_list.html", context=neirong)

#会员 电影 浏览 删除
def mem_xiangmu_liulan_del(request):
    if request.method == "GET":
        id = request.GET.get("id")
        dijiye = request.GET.get("dijiye")
        curson = connection.cursor()
        sql = "delete from xiangmu_liulan where id=%s" % id
        curson.execute(sql)
        return redirect("/mem_xiangmu_liulan_list/%s" % dijiye)
