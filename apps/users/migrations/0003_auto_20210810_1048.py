# Generated by Django 3.2.5 on 2021-08-10 02:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210809_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='uonline',
            field=models.BooleanField(default=False, verbose_name='用户是否在线'),
        ),
        migrations.AlterField(
            model_name='userchatroomstatus',
            name='last_enter_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 10, 48, 31, 860146), verbose_name='上次浏览时间'),
        ),
    ]