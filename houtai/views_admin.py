from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse
import time
from datetime import  datetime
from django.utils.timezone import make_aware
import json

def ht_admin_add(request):
    if request.method == "GET":
        # 0-id  1-fenzu_mingcheng  2-quanxian_1 3-quanxian_2  4-quanxian
        curson = connection.cursor()
        curson.execute("select * from quanxian_fenzu ")
        fenzus = curson.fetchall()
        neirong = {
            "fenzus":fenzus
        }
        return render(request,"houtai/quanxian/admin_add.html",context=neirong)

    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user_password = request.POST.get("user_password")
        beizhu = request.POST.get("beizhu")
        fenzu_id = request.POST.get("fenzu_id")
        add_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        curson = connection.cursor()
        sql = "insert into quanxian_yonghu(user_name,user_password,fenzu_id,add_date,beizhu) values ('%s','%s',%s,'%s','%s')" \
              % (user_name,user_password,fenzu_id, add_date,beizhu)
        curson.execute(sql)
        return redirect("/ht_admin_list")


def ht_admin_xiugai(request):
    if request.method == "GET":
        # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
        curson_fenzu = connection.cursor()
        curson_fenzu.execute("select * from quanxian_fenzu ")
        fenzus = curson_fenzu.fetchall()

        uid = request.GET.get("uid")
        curson = connection.cursor()
        curson.execute("select * from quanxian_yonghu where id=%s" % uid)
        info = curson.fetchone()
        print(info[3])

        neirong = {
            "fenzus":fenzus,
            "info":info,
            "fzid":info[3]
        }
        return render(request,"houtai/quanxian/admin_xiugai.html",context=neirong)


    if request.method =="POST":
        uid = request.POST.get("uid")
        #user_name = request.POST.get("user_name")
        user_password = request.POST.get("user_password")
        beizhu = request.POST.get("beizhu")
        fenzu_id = request.POST.get("fenzu_id")
        add_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
        curson = connection.cursor()
        sql = "update quanxian_yonghu set user_password='%s',fenzu_id=%s,beizhu='%s' where id=%s" % (
        user_password, fenzu_id, beizhu,uid)
        curson.execute(sql)
        return redirect("/ht_admin_list")


def ht_admin_list(request):
    shuju = ""
    shuju = shuju + ''
    shuju = shuju + '<table width="100%" bgcolor="#dcdcdc" border="1" cellspacing="0" cellpadding="0">'
    shuju = shuju + '<tr><td style="padding: 5px;font-weight: bold;" width="20%">时间</td><td style="padding: 5px;font-weight: bold;"  width="20%">账号</td>' \
                    '<td style="padding: 5px;font-weight: bold;"  width="20%">角色</td><td style="padding: 5px;font-weight: bold;"  width="20%">备注</td>' \
                    '<td style="padding: 5px;font-weight: bold;"  width="20%">操作</td></tr>'
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    curson = connection.cursor()
    curson.execute("select * from quanxian_yonghu ")
    fenzus = curson.fetchall()
    for fenzu in fenzus:
        print(fenzu)
        shuju = shuju + '<tr>'
        shuju = shuju + '<td style="background-color: #FFFFFF;padding: 5px;">%s</td>' % fenzu[4]
        shuju = shuju + '<td style="background-color: #FFFFFF;padding: 5px;">%s</td>' % fenzu[1]
        #fenzu[3]  角色<>分组   读取分组中文名称
        # 0-id  1-fenzu_mingcheng  2-quanxian_1 3-quanxian_2  4-quanxian
        curson_fenzu = connection.cursor()
        curson_fenzu.execute("select * from quanxian_fenzu where id=%s " % fenzu[3])
        fenzu_info = curson_fenzu.fetchone()

        shuju = shuju + '<td style="background-color: #FFFFFF;padding: 5px;">%s</td>' % fenzu_info[1]
        shuju = shuju + '<td style="background-color: #FFFFFF;padding: 5px;">%s</td>' % fenzu[5]
        shuju = shuju + '<td style="background-color: #FFFFFF;padding: 5px;">'
        shuju = shuju + '<a href="/ht_admin_xiugai?uid=%s">修改</a>&nbsp;&nbsp;' % fenzu[0]
        shuju = shuju + '| &nbsp;&nbsp;<a href="/ht_admin_del?uid=%s">删除</a>' % fenzu[0]
        shuju = shuju + '</td></tr>'
    shuju = shuju + '</table>'

    neirong = {
        "shuju": shuju
    }

    return render(request,"houtai/quanxian/admin_list.html",context=neirong)

def ht_admin_del(request):
    # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
    if request.method == "GET":
        uid = request.GET.get("uid")
        curson = connection.cursor()
        sql = "delete from quanxian_yonghu where id=%s" % uid
        curson.execute(sql)
        return redirect("/ht_admin_list")

#修改个人资料
def ht_admin_mima(request):
    uid = request.COOKIES.get("uid")
    uname = request.COOKIES.get("uname")

    neirong = {
        "uid":uid,
        "uname":uname,
    }
    if request.method == "GET":
        return render(request, "houtai/quanxian/admin_mima.html", context=neirong)

    if request.method == "POST":
        mm1 = request.POST.get("mm1")
        mm2 = request.POST.get("mm2")
        print(mm1 + "=========" + mm2)

        #判断原始密码是否正确
        curson = connection.cursor()
        curson.execute("select * from quanxian_yonghu where id=%s and user_password='%s' " % (request.COOKIES.get("uid"), mm1))
        info = curson.fetchone()
        if info:
            #更新密码
            curson_update = connection.cursor()
            sql_update = "update quanxian_yonghu set user_password='%s' where id=%s" % (mm2,request.COOKIES.get("uid"))
            curson_update.execute(sql_update)
            return redirect("/ht/tab")
        else:
            cuowu = "<script>alert('账号错误')</script>"
            neirong={
                "cuowu":cuowu
            }
            return render(request,"houtai/tab.html",context=neirong)

#退出
def ht_admin_logout(request):
    if request.method == "GET":
        # 写登录cookie
        shijian01 = datetime(year=2099, month=1, day=1, hour=20, minute=0, second=0)
        shijian02 = make_aware(shijian01)
        myurl = "<script language='JavaScript' >alert('成功退出！');window.parent.location='/ht';</script>"
        response = HttpResponse(myurl)
        # 0-id  1-user_name  2-user_password 3-fenzu_id  4-add_date  5-beizhu
        response.set_cookie("uid", "", expires=shijian01)
        response.set_cookie("uname", "", expires=shijian01)
        response.set_cookie("fzid", "", expires=shijian01)

        return response
        # 转发
        # return book_views.index(request)
        # 重定向
        # return HttpResponseRedirect("/ht/main")


