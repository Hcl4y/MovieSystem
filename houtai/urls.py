from django.urls import path

from django.urls import path
from django.conf.urls.static import static
from django.conf import  settings

from . import views
from . import views_quanxian
from . import views_admin
from . import views_xinwen
from . import views_upload
from . import views_huiyuan
from . import views_ad
from . import views_liuyan
from . import uploads
from . import views_chanpin
from . import views_xiangmu

urlpatterns = [

    #下面是后台管理首页-开始
    path('ht', views.ht),  #后台登录页面
    path('ht/main', views.ht_main), #登录后，后台管理首页
    path('ht/top', views.ht_top),   #登录后，后台管理首页-顶部菜单(程序化)
    path('ht/center', views.ht_center),#登录后，后台管理首页-中间布局
    path('ht/down', views.ht_down),    #登录后，后台管理首页-底部
    path('ht/middel', views.ht_middel),#登录后，后台管理首页-中间布局嵌套文件
    path('ht/left', views.ht_left),    #登录后，后台管理首页-左侧初始化页面
    path('ht/left2', views.ht_left2),  #登录后，后台管理首页-左侧菜单(程序化)
    path('ht/tab', views.ht_tab),      #登录后，后台管理首页-右侧默认页面
    #后台管理首页-结束

    #下面是后台1,2,3菜单管理-开始
    path('ht_caidan_1ji', views_quanxian.ht_caidan_1ji),        #1级菜单录入，修改
    path('ht_caidan_1ji_del', views_quanxian.ht_caidan_1ji_del),#1级菜单删除

    path("ht_caidan_2ji",views_quanxian.ht_caidan_2ji),                 #2级菜单首页，默认左侧显示1级菜单，右侧默认空
    path("ht_caidan_2ji_iframe", views_quanxian.ht_caidan_2ji_iframe),  #2级菜录入和修改
    path("ht_caidan_2ji_iframe_del", views_quanxian.ht_caidan_2ji_iframe_del),#2级菜删除

    path("ht_caidan_3ji",views_quanxian.ht_caidan_3ji),     #3级菜单首页，默认顶部显示1级和2级菜单联动操作，下面默认空
    path("ht_caidan_3ji_iframe",views_quanxian.ht_caidan_3ji_iframe),  #3级菜录入和修改
    path("ht_caidan_3ji_iframe_del", views_quanxian.ht_caidan_3ji_iframe_del), #3级菜删除

    path("ht_quanxian_list", views_quanxian.ht_quanxian_list),    #系统默认分组和对应权限列表
    path("ht_quanxian_xiugai", views_quanxian.ht_quanxian_xiugai),#分组权限设置程序
    #后台1,2,3菜单管理-结束

    #下面是后台管理员账号-开始
    path("ht_admin_add", views_admin.ht_admin_add),       #管理员账号-录入
    path("ht_admin_xiugai", views_admin.ht_admin_xiugai), #管理员账号-修改
    path("ht_admin_list", views_admin.ht_admin_list),     #管理员账号-列表
    path("ht_admin_del", views_admin.ht_admin_del),       #管理员账号-删除
    path("ht_admin_logout",views_admin.ht_admin_logout),  #当前登录管理员-退出系统
    path("ht_admin_mima", views_admin.ht_admin_mima),     #当前登录管理员-秘密修改
    #后台管理员账号-结束

    path("set_web_mc", views_ad.set_web_mc),  # 设置系统名称
    path("set_guanyu_women", views_ad.set_guanyu_women),  # 关于我们设置
    path("set_key_remen", views_ad.set_key_remen),  # 设置热门关键字,

    path("upload01", views_upload.upload01),   #图片上传模块
    path("xinwen_fenlei", views_xinwen.xinwen_fenlei),        #新闻分类-录入和修改
    path("xinwen_fenlei_del", views_xinwen.xinwen_fenlei_del),#新闻分类-删除
    path("xinwen_add", views_xinwen.xinwen_add),              #新闻中心-录入
    path("xinwen_list/<dijiye>", views_xinwen.xinwen_list),   #新闻中心-列表
    path("xinwen_del", views_xinwen.xinwen_del),              #新闻中心-删除
    path("xinwen_xiugai", views_xinwen.xinwen_xiugai),        #新闻中心-修改
    path("set_key_remen_xinwen", views_xinwen.set_key_remen_xinwen),       #新闻中心-关键字设定
    path("xinwen_pinglun_list/<dijiye>", views_xinwen.xinwen_pinglun_list),#新闻评论-列表
    path("xinwen_pinglun_chuli", views_xinwen.xinwen_pinglun_chuli),       #新闻评论-审核处理

    path("xiangmu_fenlei", views_xiangmu.xiangmu_fenlei),         #电影项目分类-录入和修改
    path("xiangmu_fenlei_del", views_xiangmu.xiangmu_fenlei_del), #电影项目分类-删除
    path("xiangmu_add", views_xiangmu.xiangmu_add),           #项目电影-录入
    path("xiangmu_list/<dijiye>", views_xiangmu.xiangmu_list),#项目电影-列表
    path("xiangmu_del", views_xiangmu.xiangmu_del),           #项目电影-删除
    path("xiangmu_xiugai", views_xiangmu.xiangmu_xiugai),     #项目电影-修改

    path("xiangmu_mulu", views_xiangmu.xiangmu_mulu), # 项目电影-目录首页
    path("mulu1_add", views_xiangmu.mulu1_add),       # 项目电影-目录 章 录入
    path("mulu1_xiugai", views_xiangmu.mulu1_xiugai), # 项目电影-目录 章 修改
    path("mulu_del", views_xiangmu.mulu_del),         # 项目电影-目录 章和节 删除
    path("mulu2_add", views_xiangmu.mulu2_add),       # 项目电影-目录 节 录入
    path("mulu2_xiugai", views_xiangmu.mulu2_xiugai), # 项目电影-目录 节 修改

    path("xiangmu_dingdan_list/<dijiye>", views_xiangmu.xiangmu_dingdan_list),  #项目电影-订单 列表
    path("xiangmu_dingdan_del", views_xiangmu.xiangmu_dingdan_del),             #项目电影-订单 删除
    path("xiangmu_pinglun_list/<dijiye>", views_xiangmu.xiangmu_pinglun_list),  #项目电影-评论 列表
    path("xiangmu_pinglun_chuli", views_xiangmu.xiangmu_pinglun_chuli),         #项目电影-评论 删除

    path("huiyuan_fenlei", views_huiyuan.huiyuan_fenlei),
    path("huiyuan_fenlei_del", views_huiyuan.huiyuan_fenlei_del),
    path("huiyuan_list/<dijiye>", views_huiyuan.huiyuan_list),  #会员列表
    path("huiyuan_del", views_huiyuan.huiyuan_del),             #会员删除

    path("ad", views_ad.ad_xiugai),   #设置轮播图广告
    path("liuyan_list/<dijiye>", views_liuyan.liuyan_list), #留言列表
    path("liuyan_del", views_liuyan.liuyan_del),            #留言删除

    #path("set_key_remen_chanpin", views_chanpin.set_key_remen_chanpin), #设置公司环境热门关键字
    path("chanpin_fenlei", views_chanpin.chanpin_fenlei),               #公司环境分类-录入和修改
    path("chanpin_fenlei_del", views_chanpin.chanpin_fenlei_del),       #公司环境分类-删除
    path("chanpin_list/<dijiye>", views_chanpin.chanpin_list),          #公司环境-列表
    path("chanpin_add", views_chanpin.chanpin_add),                     #公司环境-录入
    path("chanpin_del", views_chanpin.chanpin_del),                     #公司环境-删除
    path("chanpin_xiugai", views_chanpin.chanpin_xiugai),               #公司环境-修改
    path("chanpin_pinglun_list/<dijiye>", views_chanpin.chanpin_pinglun_list), #公司环境评论-列表
    path("chanpin_pinglun_chuli", views_chanpin.chanpin_pinglun_chuli),        #公司环境评论-审核处理

    #下面是第3方在线编辑器，上传模块
    path("upload_image", uploads.upload_image),
    path("upload_generation_dir", uploads.upload_generation_dir),
    path("image_upload", uploads.image_upload),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
