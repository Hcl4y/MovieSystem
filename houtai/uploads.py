from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt

#  http://127.0.0.1:8000/upload/kindeditor?dir=image

@csrf_exempt
def upload_image(request):
    # file_path = os.path.join('media/tupian/', timestamp + myfile.name)
    result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)
    if files:
        #result = image_upload(files, os.path.join('media/tupian'))
        result = image_upload(files)
    return HttpResponse(json.dumps(result), content_type="application/json")
# 目录创建

def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/' % (today.year, today.month)
    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
        os.makedirs(settings.MEDIA_ROOT + dir_name)
    return dir_name

# 图片上传
def image_upload(files):
    # 允许上传文件类型
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif',
                    'bmp', 'zip', "swf", "flv",
                    "mp3", "wav", "wma", "wmv",
                    "mid", "avi", "mpg", "asf",
                    "rm", "rmvb", "doc", "docx",
                    "xls", "xlsx", "ppt", "htm",
                    "html", "txt", "zip", "rar",
                    "gz", "bz2"]
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    # relative_path_file = upload_generation_dir(dir_name)
    # print(relative_path_file)

    # path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    # print("path = %s" % path)
    #
    # if not os.path.exists(path):  # 如果目录不存在创建目录
    #     os.makedirs(path)

    file_name = str(uuid.uuid1()) + "." + file_suffix
    print("file_name = %s" % file_name)

    # path_file = os.path.join(path, file_name)
    # print("path_file = %s" % path_file)

    #file_url = settings.MEDIA_URL + relative_path_file + file_name
    file_url =  file_name
    print("file_url = %s" % file_url)

    file_path00000 = os.path.join('media/tupian/',file_url )
    print("file_path00000 = %s" % file_path00000)

    open(file_path00000, 'wb').write(files.file.read())

   #  http://127.0.0.1:8000/media/media/tupian/2021/12/65123fb3-69fa-11ec-be05-b06ebf384b20.png
    #return {"error": 0, "url": file_url}

    #return {"error": 0, "url": "http://127.0.0.1:8000/media/media/tupian/2021/12/65123fb3-69fa-11ec-be05-b06ebf384b20.png"}

    return {"error": 0,
            "url": "http://127.0.0.1:8000/" + file_path00000}