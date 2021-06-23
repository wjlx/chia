# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 
:File    : 
"""

from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    """
    用户管理
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'password')


class UserKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKey
        fields = ('id', 'user', 'fingerprint', 'master_public_key',
                  'farmer_public_key', 'pool_public_key', 'first_wallet_address')

    @staticmethod
    def get_user(obj):
        if obj.user:
            return obj.user.username
        return ''


class PlotsTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotsTask
        fields = ('id', 'user_key', 'plot_size', 'num', 'buffer',
                  'num_threads', 'buckets', 'tmp_dir', 'tmp2_dir', 'final_dir')

    @staticmethod
    def get_user_key(obj):
        if obj.user_key:
            return obj.user_key.id
        return ''


class PlotsTaskControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotsTaskControl
        fields = ('id', 'plots_task', 'status')

    @staticmethod
    def get_plots_task(obj):
        if obj.plots_task:
            return obj.plots_task.id
        return ''


class PlotsTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotsTaskResult
        fields = ('id', 'plots_task', 'total_block', 'finished_block')

    @staticmethod
    def get_plots_task(obj):
        if obj.plots_task:
            return obj.plots_task.id
        return ''

    # def create(self, validated_data):
    #     plots_task = validated_data['plots_task']
    #     pt = PlotsTaskResult.objects.filter(plots_task__id=plots_task.id)
    #     if pt:
    #         pt.update(**validated_data)
    #     else:
    #         pt = PlotsTaskResult.objects.create(**validated_data)
    #     return pt
