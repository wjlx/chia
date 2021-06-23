# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

import xadmin
from xadmin import views
from xadmin.plugins.actions import BaseActionView
from django.http.response import HttpResponse

from .models import UserKey, PlotsTask, PlotsTaskControl, PlotsTaskResult


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = ""  # 设置站点标题
    site_footer = ""  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

    # def get_site_menu(self, obj):
    #     return [
    #         {'title': '课程管理', 'menus': [
    #             {'title': '课程信息', 'url': ""},
    #             {'title': '章节信息', 'url': ""},
    #             {'title': '视频信息', 'url': ""},
    #             {'title': '课程资源', 'url': ""},
    #             {'title': '课程评论', 'url': ""},
    #         ]},
    #     ]


xadmin.site.register(views.CommAdminView, GlobalSettings)


class UserKeyModelAdmin(object):
    list_display = [
        "id",
        "get_user",
        "fingerprint",
        "master_public_key",
        "farmer_public_key",
        "pool_public_key",
        "first_wallet_address",
        "create_at",
        "update_at",
    ]
    search_fields = ['user__username', "fingerprint"]
    list_filter = ['user__username', "fingerprint"]
    show_detail_fields = ('get_user',)
    list_display_links = ['get_user']
    refresh_times = [10, 60]
    list_per_page = 20
    actions = ['to_excel']

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = "用户名"

    def save_models(self):
        obj = self.new_obj
        print("@" * 100)
        obj.save()


class PlotsTaskModelAdmin(object):
    list_display = [
        "id",
        "get_user_fingerprint",
        "plot_size",
        "num",
        "buffer",
        "num_threads",
        "buckets",
        "tmp_dir",
        "tmp2_dir",
        "final_dir",
        "create_at",
        "update_at",
    ]
    search_fields = ['id', "user_key__fingerprint"]
    list_filter = ['id', "user_key__fingerprint"]
    list_editable = ['tmp_dir', 'tmp2_dir', 'final_dir']
    raw_id_fields = ('user',)
    model_icon = 'fa fa-user-secret'
    list_per_page = 20

    def get_user_fingerprint(self, obj):
        return obj.user_key.fingerprint

    get_user_fingerprint.short_description = "用户指纹"


class MyAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "my_action"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = 'Test selected %(verbose_name_plural)s'

    model_perm = 'change'  #: 该 Action 所需权限

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        # queryset 是包含了已经选择的数据的 queryset
        for obj in queryset:
            # obj 的操作
            ...
        # 返回 HttpResponse
        return HttpResponse("successful")


class PlotsTaskControlModelAdmin(object):
    list_display = [
        "id",
        "get_plots_task_id",
        "status",
        "create_at",
        "update_at",
    ]
    search_fields = ['id', "plots_task__id"]
    list_filter = ['id', "plots_task__id"]
    actions = [MyAction, ]

    def get_plots_task_id(self, obj):
        return obj.plots_task.id

    get_plots_task_id.short_description = "绘图任务ID"


class PlotsTaskResultModelAdmin(object):
    list_display = [
        "id",
        "get_plots_task",
        "total_block",
        "finished_block",
        "get_rate",
        "create_at",
        "update_at",
    ]
    search_fields = ['id', "plots_task__id", "plots_task__user_key__fingerprint"]
    list_filter = ['id', "plots_task__id", "plots_task__user_key__fingerprint"]
    list_per_page = 20
    refresh_times = [5, 10]

    def get_plots_task(self, obj):
        return obj.plots_task.id

    get_plots_task.short_description = "绘图任务ID"

    def get_rate(self, obj):
        if obj.finished_block == 0:
            return "0%"
        else:
            return f"{(obj.finished_block / obj.total_block) * 100}%"

    get_rate.short_description = "执行进度"


xadmin.site.register(UserKey, UserKeyModelAdmin)
xadmin.site.register(PlotsTask, PlotsTaskModelAdmin)
xadmin.site.register(PlotsTaskControl, PlotsTaskControlModelAdmin)
xadmin.site.register(PlotsTaskResult, PlotsTaskResultModelAdmin)
