from django.urls import path

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from . import zixun
from . import xiangmu

urlpatterns = [
                  path('', views.pc_index),

                  # 下面是会员框架的基础模块，注册，登录......
                  path('mem_reg', views.mem_reg),  # 会员注册
                  path('mem_login', views.mem_login),  # 会员登录
                  path('mem_main', views.mem_main),  # 会员中心-首页
                  path('mem_logout', views.mem_logout),  # 会员中心-退出登录
                  path('mem_xinxi_xiugai', views.mem_xinxi_xiugai),  # 会员中心-用户信息修改
                  path('mem_mima', views.mem_mima),  # 会员中心-密码修改

                  path('guanyu_women', views.guanyu_women),  # 关于我们
                  path('guanyu_liuyan', views.guanyu_liuyan),  # 留言反馈
                  path('xinxi_xiangqing', zixun.xinxi_xiangqing),  # 资讯信息-详情
                  path('xinxi_list/<dijiye>/<leixing_id>', zixun.xinxi_list),  # 资讯信息-列表
                  path('zixun_index', zixun.zixun_index),  # 资讯首页
                  path('api_zixun_shoucang', zixun.api_zixun_shoucang),  # 资讯-收藏接口
                  path('api_zixun_pinglun_add', zixun.api_zixun_pinglun_add),  # 资讯-评论接口

                  path('pc_chanpin_list/<dijiye>/<leixing_id>', views.pc_chanpin_list),  # 环境列表
                  path('pc_chanpin_xiangqing', views.pc_chanpin_xiangqing),  # 环境详情
                  path('api_chanpin_shoucang', views.api_chanpin_shoucang),  # 环境会员收藏接口
                  path('api_chanpin_pinglun_add', views.api_chanpin_pinglun_add),  # 环境会员评论接口

                  path('chaxun', xiangmu.chaxun),  # 热门产品查询跳转程序
                  path('pc_xiangmu_list/<dijiye>/<leixing_id>', xiangmu.pc_xiangmu_list),  # 项目 电影 列表
                  path('pc_xiangmu_xiangqing', xiangmu.pc_xiangmu_xiangqing),  # 项目 电影 详情
                  path('pc_xiangmu_ding', xiangmu.pc_xiangmu_ding),  # 项目 电影 电影票 选座购买界面
                  path('api_xiangmu_ding_add', xiangmu.api_xiangmu_ding_add),  # 项目 电影 电影票 下单

                  path('api_xiangmu_dingdan_del', xiangmu.api_xiangmu_dingdan_del),  # 项目 电影 电影票 取消删除
                  path('api_xiangmu_dingdan_fukuan', xiangmu.api_xiangmu_dingdan_fukuan),  # 项目 电影 电影票 模拟付款
                  path('api_xiangmu_shoucang', xiangmu.api_xiangmu_shoucang),  # 项目 电影 收藏
                  path('api_xiangmu_pinglun_add', xiangmu.api_xiangmu_pinglun_add),  # 项目 电影 评论

                  path("mem_xiangmu_dingdan_list/<dijiye>", xiangmu.mem_xiangmu_dingdan_list),  # 会员中心-电影-订单列表
                  path("mem_xiangmu_shoucang_list/<dijiye>", xiangmu.mem_xiangmu_shoucang_list),  # 会员中心-电影-收藏列表
                  path("mem_xiangmu_shoucang_del", xiangmu.mem_xiangmu_shoucang_del),  # 会员中心-电影-收藏删除
                  path("mem_xiangmu_pinglun_list/<dijiye>", xiangmu.mem_xiangmu_pinglun_list),  # 会员中心-电影-评论列表
                  path("mem_xiangmu_pinglun_del", xiangmu.mem_xiangmu_pinglun_del),  # 会员中心-电影-评论删除
                  path("mem_xiangmu_liulan_list/<dijiye>", xiangmu.mem_xiangmu_liulan_list),  # 会员中心-电影-浏览记录列表
                  path("mem_xiangmu_liulan_del", xiangmu.mem_xiangmu_liulan_del),  # 会员中心-电影-浏览记录删除

                  path('mem_chanpin_shoucang_del', views.mem_chanpin_shoucang_del),  # 环境 会员 收藏 删除
                  path("mem_chanpin_shoucang_list/<dijiye>", views.mem_chanpin_shoucang_list),  # 环境 会员 收藏 列表
                  path('mem_chanpin_pinglun_del', views.mem_chanpin_pinglun_del),  # 环境 会员 评论 删除
                  path("mem_chanpin_pinglun_list/<dijiye>", views.mem_chanpin_pinglun_list),  # 环境 会员 评论 列表

                  path("mem_zixun_shoucang_list/<dijiye>", zixun.mem_zixun_shoucang_list),  # 会员中心-资讯-收藏列表
                  path("mem_zixun_shoucang_del", zixun.mem_zixun_shoucang_del),  # 会员中心-资讯-收藏删除
                  path("mem_zixun_pinglun_list/<dijiye>", zixun.mem_zixun_pinglun_list),  # 会员中心-资讯-评论列表
                  path("mem_zixun_pinglun_del", zixun.mem_zixun_pinglun_del),  # 会员中心-资讯-评论删除
                  path("mem_zixun_liulan_list/<dijiye>", zixun.mem_zixun_liulan_list),  # 会员中心-资讯-浏览记录列表
                  path("mem_zixun_liulan_del", zixun.mem_zixun_liulan_del)  # 会员中心-资讯-浏览记录删除

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
