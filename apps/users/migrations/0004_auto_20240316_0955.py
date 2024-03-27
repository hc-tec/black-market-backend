# Generated by Django 3.0.4 on 2024-03-16 01:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210810_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='qq',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='contact',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='联系方式'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userchatroomstatus',
            name='last_enter_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 16, 9, 55, 16, 86262), verbose_name='上次浏览时间'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='school_zone',
            field=models.IntegerField(choices=[(1, '主校区'), (2, '同济校区'), (3, '网安校区'), (4, '东湖校区'), (5, '青山湖校区'), (6, '鄱阳湖校区'), (7, '抚州校区')], default=1, verbose_name='校区'),
        ),
    ]
