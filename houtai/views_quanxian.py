from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse


def ht_caidan_1ji(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        row_edit = ""
        #如果是修改，则读取要修改的内容
        if id_1ji:
            curson_edit = connection.cursor()
            sql_edit = "select * from quanxian_caidan where id=%s" % id_1ji
            curson_edit.execute(sql_edit)
            row_edit = curson_edit.fetchone()

        #读取所有1级菜单
        curson = connection.cursor()
        curson.execute("select * from quanxian_caidan where caidan_jibie=1")
        rows = curson.fetchall()
        neirong = {
            "caidan_1jis": rows,
            "id_1ji":id_1ji,
            "caidan_info":row_edit
        }
        return render(request, "houtai/quanxian/caidan_1ji.html", context=neirong)

    if request.method == "POST":
        #判断id_1ji，有值则是修改，没有则是新录入
        id_1ji = request.POST.get("id_1ji")
        if id_1ji:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "update quanxian_caidan set caidan_mingcheng='%s',paixu_id=%s where id=%s" % (caidan_mingcheng,paixu_id,id_1ji)
            curson.execute(sql)
        else:
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "insert into quanxian_caidan(caidan_mingcheng,caidan_jibie,caidan_suoshu,paixu_id) values ('%s',1,0,%s)" % (
            caidan_mingcheng, paixu_id)
            curson.execute(sql)
        return redirect("/ht_caidan_1ji")

#表：0-id    1-caidan_mingcheng   2-caidan_lujing   3-caidan_jibie   4-caidan_suoshu   5-paixu_id
def ht_caidan_1ji_del(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        curson = connection.cursor()
        sql = "delete from quanxian_caidan where id=%s" % id_1ji
        curson.execute(sql)
        return redirect("/ht_caidan_1ji")

#2级权限菜单 主页面
def ht_caidan_2ji(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        row_edit = ""
        #如果是修改，则读取要修改的内容
        if id_1ji:
            curson_edit = connection.cursor()
            sql_edit = "select * from quanxian_caidan where id=%s" % id_1ji
            curson_edit.execute(sql_edit)
            row_edit = curson_edit.fetchone()

        #读取所有1级菜单
        curson = connection.cursor()
        curson.execute("select id,caidan_mingcheng from quanxian_caidan where caidan_jibie=1")
        rows = curson.fetchall()
        neirong = {
            "caidan_1jis": rows,
            "id_1ji":id_1ji,
            "caidan_info":row_edit
        }
        return render(request, "houtai/quanxian/caidan_2ji.html", context=neirong)

#2级权限菜单 内嵌iframe页面
def ht_caidan_2ji_iframe(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        row_edit = ""  #存修改数据

        id_2ji = request.GET.get("id_2ji")
        #如果是修改，则读取要修改的内容2级菜单内容
        if id_2ji:
            curson_edit = connection.cursor()
            sql_edit = "select * from quanxian_caidan where id=%s" % id_2ji
            curson_edit.execute(sql_edit)
            row_edit = curson_edit.fetchone()

        #读取传递过来的1级id下面的 > 所有2级菜单  -------------------111111111
        curson = connection.cursor()
        curson.execute("select * from quanxian_caidan where caidan_jibie=2 and caidan_suoshu=%s" % id_1ji)
        rows = curson.fetchall()
        neirong = {
            "caidan_2jis": rows,
            "id_1ji":id_1ji,
            "id_2ji": id_2ji,
            "caidan_info":row_edit
        }
        return render(request, "houtai/quanxian/caidan_2ji_iframe.html", context=neirong)

    if request.method == "POST":
        #判断id_2ji，有值则是修改，没有则是新录入
        id_1ji = request.POST.get("id_1ji") #1级菜单id
        id_2ji = request.POST.get("id_2ji")
        if id_2ji: #更新2级菜单  程序
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "update quanxian_caidan set caidan_mingcheng='%s',paixu_id=%s where id=%s" % (caidan_mingcheng,paixu_id,id_2ji)
            curson.execute(sql)
        else: #录入2级菜单  程序
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "insert into quanxian_caidan(caidan_mingcheng,caidan_jibie,caidan_suoshu,paixu_id) values ('%s',2,%s,%s)" % (
            caidan_mingcheng,id_1ji, paixu_id)
            curson.execute(sql)
        url = "/ht_caidan_2ji_iframe?id_1ji=%s" % id_1ji
        return redirect(url)

#表：0-id    1-caidan_mingcheng   2-caidan_lujing   3-caidan_jibie   4-caidan_suoshu   5-paixu_id
def ht_caidan_2ji_iframe_del(request):
    if request.method == "GET":
        id_1ji = request.GET.get("id_1ji")
        id_2ji = request.GET.get("id_2ji") #2级菜单的id
        curson = connection.cursor()
        sql = "delete from quanxian_caidan where id=%s and caidan_suoshu=%s and caidan_jibie=2" %(id_2ji,id_1ji)
        curson.execute(sql)
        return redirect("/ht_caidan_2ji_iframe?id_1ji=%s" % id_1ji)

############################################################################################################
#3级权限菜单
def ht_caidan_3ji(request):
    if request.method == "GET":
        neirong = {}
        id_1ji = request.GET.get("id_1ji")
        id_2ji = request.GET.get("id_2ji")
        rows_1ji = ""
        rows_2ji = ""
        #读取所有1级菜单
        curson = connection.cursor()
        curson.execute("select id,caidan_mingcheng from quanxian_caidan where caidan_jibie=1")
        rows_1ji = curson.fetchall()

        #读取1级菜单下的 所有2级菜单
        if id_1ji:
            curson = connection.cursor()
            curson.execute("select id,caidan_mingcheng from quanxian_caidan where caidan_jibie=2 and caidan_suoshu=%s" % id_1ji)
            rows_2ji = curson.fetchall()

        neirong = {
            "caidan_1jis": rows_1ji,
            "id_1ji": id_1ji,
            "caidan_2jis": rows_2ji,
            "id_2ji": id_2ji,
        }

        return render(request, "houtai/quanxian/caidan_3ji.html", context=neirong)

#3级权限菜单 内嵌iframe页面
def ht_caidan_3ji_iframe(request):
    if request.method == "GET":
        id_2ji = request.GET.get("id_2ji")
        row_edit = ""  #存修改数据

        id_3ji = request.GET.get("id_3ji")
        #如果是修改，则读取要修改的内容2级菜单内容
        if id_3ji:
            curson_edit = connection.cursor()
            sql_edit = "select * from quanxian_caidan where id=%s" % id_3ji
            curson_edit.execute(sql_edit)
            row_edit = curson_edit.fetchone()

        #读取传递过来的2级id下面的 > 所有3级菜单  -------------------
        curson = connection.cursor()
        curson.execute("select * from quanxian_caidan where caidan_jibie=3 and caidan_suoshu=%s" % id_2ji)
        rows = curson.fetchall()
        neirong = {
            "caidan_3jis": rows,
            "id_2ji":id_2ji,
            "id_3ji": id_3ji,
            "caidan_info":row_edit
        }
        return render(request, "houtai/quanxian/caidan_3ji_iframe.html", context=neirong)

    if request.method == "POST":
        #判断id_3ji，有值则是修改，没有则是新录入
        id_2ji = request.POST.get("id_2ji") #2级菜单id
        id_3ji = request.POST.get("id_3ji")
        if id_3ji: #更新3级菜单  程序
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            caidan_lujing = request.POST.get("caidan_lujing")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "update quanxian_caidan set caidan_mingcheng='%s',caidan_lujing='%s',paixu_id=%s where id=%s" % (caidan_mingcheng,caidan_lujing,paixu_id,id_3ji)
            curson.execute(sql)
        else: #录入3级菜单  程序
            caidan_mingcheng = request.POST.get("caidan_mingcheng")
            caidan_lujing = request.POST.get("caidan_lujing")
            paixu_id = request.POST.get("paixu_id")
            curson = connection.cursor()
            sql = "insert into quanxian_caidan(caidan_mingcheng,caidan_lujing,caidan_jibie,caidan_suoshu,paixu_id) values ('%s','%s',3,%s,%s)" % (
            caidan_mingcheng,caidan_lujing,id_2ji, paixu_id)
            curson.execute(sql)
        url = "/ht_caidan_3ji_iframe?id_2ji=%s" % id_2ji
        return redirect(url)

def ht_caidan_3ji_iframe_del(request):
    if request.method == "GET":
        id_2ji = request.GET.get("id_2ji")
        id_3ji = request.GET.get("id_3ji") #3级菜单的id
        curson = connection.cursor()
        sql = "delete from quanxian_caidan where id=%s and caidan_suoshu=%s and caidan_jibie=3" %(id_3ji,id_2ji)
        curson.execute(sql)
        return redirect("/ht_caidan_3ji_iframe?id_2ji=%s" % id_2ji)

################################################权限管理################################################
#现有分组列表 + 权限列表
def ht_quanxian_list(request):
    if request.method == "GET":
        neirong = {}

        curson = connection.cursor()
        sql = "select * from quanxian_fenzu "
        # 0-id  1-fenzu_mingcheng  2-quanxian_1 3-quanxian_2  4-quanxian
        curson.execute(sql)
        fenzu_list = curson.fetchall()

        fenzu = ""
        fenzu = fenzu + ''
        fenzu = fenzu + '<table width="100%" border="1" cellpadding="0" cellspacing="0">'
        fenzu = fenzu + '<tr><td width="15%"><b>角色</b></td><td width="70%"><b>权限</b></td><td width="15%"><b>操作</b></td></tr>'
        fenzu = fenzu + ''


        #0-id  1-fenzu_mingcheng  2-quanxian_1 3-quanxian_2  4-quanxian_3
        for x in fenzu_list:
            print("%s | %s | %s | %s | %s | %s" % (x,x[0],x[1],x[2],x[3],x[4]))
            print("="*100)
            #print("-" * 100)
            #x[2] 代表1级权限， x[3] 代表2级权限， x[4] 代表3级权限，

            fenzu = fenzu + '<tr>'
            fenzu = fenzu + '<td>%s</td>' % x[1]
            fenzu = fenzu + '<td>'
            # 读取所有1级菜单
            curson_1ji = connection.cursor()
            sql_1ji = "select * from quanxian_caidan where caidan_jibie=1 and id in(0%s0)"%x[2]
            print(sql_1ji)
            curson_1ji.execute(sql_1ji)
            list1 = curson_1ji.fetchall()
            caidan = ""
            for row1 in list1:
                caidan = caidan + "<b>" + row1[1] + "</b><br> "
                print(row1[1])

                # 读取该1级菜单下  > 所有2级菜单
                curson_2ji = connection.cursor()
                sql_2ji = "select * from quanxian_caidan where caidan_jibie=2 and caidan_suoshu=%s  and id in(0%s0)"  % (row1[0],x[3])
                print(sql_2ji)
                curson_2ji.execute(sql_2ji)
                list2 = curson_2ji.fetchall()
                for row2 in list2:
                    caidan = caidan + "---" + row2[1] + "---<br> "
                    print(row2[1])

                    # 读取该2级菜单下  > 所有3级菜单
                    curson_3ji = connection.cursor()
                    sql_3ji = "select * from quanxian_caidan where caidan_jibie=3 and caidan_suoshu=%s and id in(0%s0)" % (row2[0],x[4])
                    print(sql_3ji)
                    curson_3ji.execute(sql_3ji)
                    list3 = curson_3ji.fetchall()
                    for row3 in list3:
                        print(row3[1])
                        caidan = caidan + row3[1] + "  | "
                    caidan = caidan + "<br>"

            fenzu = fenzu + caidan
            fenzu = fenzu + '</td>'
            fenzu = fenzu + '<td><a href="/ht_quanxian_xiugai?fenzu_id=%s">配置该分组权限</a></td>' % x[0]
            fenzu = fenzu + '</tr>'

        fenzu = fenzu + '</table>'

        neirong = {
            "fenzu":fenzu,
        }

    return render(request,"houtai/quanxian/quanxian_list.html",context=neirong)


def ht_quanxian_xiugai(request):
    if request.method == "GET":
        fenzu_id =request.GET.get("fenzu_id") #分组id
        #根据分组id > 读取对应的1,2,3级的权限，用于后面判断是否选中
        curson_fenzu = connection.cursor()
        sql_fenzu = "select * from quanxian_fenzu where id=%s" % fenzu_id
        curson_fenzu.execute(sql_fenzu)
        row_fenzu = curson_fenzu.fetchone()
        fenzu_quanxian1 =  row_fenzu[2]
        fenzu_quanxian2 = row_fenzu[3]
        fenzu_quanxian3 = row_fenzu[4]

        # 读取所有1级菜单
        curson_1ji = connection.cursor()
        sql_1ji = "select * from quanxian_caidan where caidan_jibie=1"
        curson_1ji.execute(sql_1ji)
        list1 = curson_1ji.fetchall()
        caidan = ""
        for row1 in list1:
            caidan = caidan + "<b>" +  row1[1] + "</b><br> "

            # 读取该1级菜单下  > 所有2级菜单
            curson_2ji = connection.cursor()
            sql_2ji = "select * from quanxian_caidan where caidan_jibie=2 and caidan_suoshu=%s" % row1[0]
            curson_2ji.execute(sql_2ji)
            list2 = curson_2ji.fetchall()
            for row2 in list2:
                caidan = caidan + "---" + row2[1] + "---<br> "

                # 读取该2级菜单下  > 所有3级菜单
                curson_3ji = connection.cursor()
                sql_3ji = "select * from quanxian_caidan where caidan_jibie=3 and caidan_suoshu=%s" % row2[0]
                curson_3ji.execute(sql_3ji)
                list3 = curson_3ji.fetchall()
                for row3 in list3:
                    tmp =",%s,"%row3[0]
                    if tmp in fenzu_quanxian3:
                        caidan = caidan + "<input type='checkbox' name='quanxian' value='%s' checked  />" % row3[0] + row3[1] + " "
                    else:
                        caidan = caidan + "<input type='checkbox' name='quanxian' value='%s' />" % row3[0] + row3[1] + " "


                caidan = caidan +  "<br>"

        neirong = {
            "myhtml":caidan,
            "fenzu_id":fenzu_id
        }
        return render(request,"houtai/quanxian/quanxian_xiugai.html",context=neirong)

    if request.method == "POST":
        quanxian = request.POST.getlist("quanxian")  #['337', '338', '331']

        quanxian3 = ""
        for x in quanxian:
            quanxian3 = quanxian3 + x + ","
        quanxian3 = "," + quanxian3
        print("3级菜单id=" + quanxian3)

        #3级权限，逆推到2级权限，然后逆推到1级权限
        #读取所有3级菜单，获得对应的2级菜单
        quanxian2 = ","
        tmp2 = ""
        curson_3ji = connection.cursor()
        sql_3ji = "select * from quanxian_caidan where caidan_jibie=3 and id in(0%s0)"% quanxian3
        curson_3ji.execute(sql_3ji)
        list3 = curson_3ji.fetchall()
        for row3 in list3:
            print(row3[4])
            tmp2 = ",%s,"%row3[4]
            if  tmp2 in quanxian2:
                pass
            else:
                quanxian2 = quanxian2 + str(row3[4]) + ","
        print("2级菜单id=" + quanxian2)

        quanxian1 = ","
        tmp1 = ""
        curson_2ji = connection.cursor()
        sql_2ji = "select * from quanxian_caidan where caidan_jibie=2 and id in(0%s0)"% quanxian2
        curson_2ji.execute(sql_2ji)
        list2 = curson_2ji.fetchall()
        for row2 in list2:
            print(row2[4])
            tmp1 = ",%s,"%row2[4]
            if  tmp1 in quanxian1:
                pass
            else:
                quanxian1 = quanxian1 + str(row2[4]) + ","
        print("1级菜单id=" + quanxian1)

        #更新数据库
        fenzu_id = request.POST.get("fenzu_id")
        curson = connection.cursor()
        sql = "update quanxian_fenzu set quanxian_1='%s',quanxian_2='%s',quanxian_3='%s' where id=%s" % (
        quanxian1, quanxian2, quanxian3,fenzu_id)
        curson.execute(sql)


        return redirect("/ht_quanxian_list")