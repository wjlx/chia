# Generated by Django 3.2.4 on 2021-06-20 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlotsTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('plot_size', models.IntegerField(default=32, verbose_name='绘图大小')),
                ('num', models.IntegerField(default=1, verbose_name='绘图数量')),
                ('buffer', models.IntegerField(default=1, verbose_name='缓存大小')),
                ('num_threads', models.IntegerField(default=2, verbose_name='线程数量')),
                ('buckets', models.IntegerField(default=128, verbose_name='buckets数量')),
                ('tmp_dir', models.CharField(max_length=200, verbose_name='临时目录')),
                ('tmp2_dir', models.CharField(blank=True, max_length=200, verbose_name='临时目录2')),
                ('final_dir', models.CharField(max_length=200, verbose_name='最终目录')),
            ],
            options={
                'verbose_name': '绘图任务',
                'verbose_name_plural': '绘图任务',
            },
        ),
        migrations.CreateModel(
            name='UserKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('fingerprint', models.CharField(max_length=20, unique=True, verbose_name='指纹')),
                ('master_public_key', models.CharField(blank=True, max_length=200, verbose_name='主公钥')),
                ('farmer_public_key', models.CharField(blank=True, max_length=200, verbose_name='农夫公钥')),
                ('pool_public_key', models.CharField(blank=True, max_length=200, verbose_name='池公钥')),
                ('first_wallet_address', models.CharField(blank=True, max_length=100, verbose_name='钱包地址1')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名')),
            ],
            options={
                'verbose_name': '用户秘钥',
                'verbose_name_plural': '用户秘钥',
            },
        ),
        migrations.CreateModel(
            name='PlotsTaskResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('total_block', models.IntegerField(verbose_name='总块数')),
                ('finished_block', models.IntegerField(verbose_name='当前块数')),
                ('plots_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plots.plotstask', verbose_name='绘图任务')),
            ],
            options={
                'verbose_name': '绘图任务进度',
                'verbose_name_plural': '绘图任务进度',
            },
        ),
        migrations.CreateModel(
            name='PlotsTaskControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20, verbose_name='任务状态')),
                ('plots_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plots.plotstask', verbose_name='任务ID')),
            ],
            options={
                'verbose_name': '绘图任务控制',
                'verbose_name_plural': '绘图任务控制',
            },
        ),
        migrations.AddField(
            model_name='plotstask',
            name='user_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plots.userkey', verbose_name='用户秘钥'),
        ),
    ]
