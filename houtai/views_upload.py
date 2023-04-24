import os
import time
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse


def upload01(request):
    if request.method == "GET":
        domid = request.GET.get("domid")
        neirong = {
            "domid": domid
        }
        return render(request, "houtai/upload/upload01.html", context=neirong)

    if request.method == "POST":
        myfile = request.FILES.get('myfile')
        domid = request.POST.get("domid")
        print("domid=" + domid)
        # imgfile.size 文件大小    做文件上传大小限制
        # imgfile.content_type 文件类型  做文件上传类型限制
        # imgfile.name 文件名称
        print(myfile)
        print(myfile.size)
        print(myfile.content_type)
        print(myfile.name)

        t = time.time()
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
        timestamp = timestamp + "-" + str(round(t))
        print(timestamp)

        # file_path = os.path.join('media/tupian/', myfile.name)
        file_path = os.path.join('media/tupian/', timestamp + myfile.name)
        print(file_path)
        with open(file_path, 'wb') as f:
            for chunk in myfile.chunks():
                f.write(chunk)

        neirong = {
            "imgs": file_path
        }

        # myurl = "<script language='JavaScript' >alert('成功退出！');window.parent.location='/ht';</script>"
        myurl = "<script language='JavaScript' >window.parent.document.form1.%s.value='%s';</script>" % (
            domid, file_path)
        response = HttpResponse(myurl)
        return response

        # return render(request,"houtai/upload/upload01.html",context=neirong)
