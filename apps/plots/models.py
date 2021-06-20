# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from django.contrib.auth.models import User
from django.db import models

from django.utils.html import format_html


class Base(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserKey(Base):
    fingerprint = models.CharField(max_length=20, unique=True, verbose_name="指纹")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户名")
    master_public_key = models.CharField(max_length=200, blank=True, verbose_name="主公钥")
    farmer_public_key = models.CharField(max_length=200, blank=True, verbose_name="农夫公钥")
    pool_public_key = models.CharField(max_length=200, blank=True, verbose_name="池公钥")
    first_wallet_address = models.CharField(max_length=100, blank=True, verbose_name="钱包地址1")

    class Meta:
        verbose_name = "用户秘钥"
        verbose_name_plural = verbose_name
        # unique_together = ('field1', 'field2',)


class PlotsTask(Base):
    user_key = models.ForeignKey(UserKey, on_delete=models.CASCADE, verbose_name="用户秘钥")
    plot_size = models.IntegerField(default=32, verbose_name="绘图大小")
    num = models.IntegerField(default=1, verbose_name="绘图数量")
    buffer = models.IntegerField(default=1, verbose_name="缓存大小")
    num_threads = models.IntegerField(default=2, verbose_name="线程数量")
    buckets = models.IntegerField(default=128, verbose_name="buckets数量")
    tmp_dir = models.CharField(max_length=200, verbose_name="临时目录")
    tmp2_dir = models.CharField(max_length=200, blank=True, verbose_name="临时目录2")
    final_dir = models.CharField(max_length=200, verbose_name="最终目录")

    class Meta:
        verbose_name = "绘图任务"
        verbose_name_plural = verbose_name

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            self.tmp_dir,
            self.tmp2_dir,
        )


class PlotsTaskControl(Base):
    TASK_STATUS = [
        ("unpublished", "未发布"),
        ("running", "执行中"),
        ("finished", "已完成"),
    ]
    plots_task = models.ForeignKey(PlotsTask, on_delete=models.CASCADE, verbose_name="任务ID")
    status = models.CharField(max_length=20, default="unpublished", verbose_name="任务状态")

    class Meta:
        verbose_name = "绘图任务控制"
        verbose_name_plural = verbose_name


class PlotsTaskResult(Base):
    plots_task = models.ForeignKey(PlotsTask, on_delete=models.CASCADE, verbose_name="绘图任务")
    total_block = models.IntegerField(verbose_name="总块数")
    finished_block = models.IntegerField(verbose_name="当前块数")

    class Meta:
        verbose_name = "绘图任务进度"
        verbose_name_plural = verbose_name
