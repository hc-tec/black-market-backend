import os
from django.db import models
from SecondaryMarket import settings

class SCHOOL_ZONE_ENUM:
    MAIN = 1
    TONG_JI = 2
    WANG_AN = 3
    JUN_SHAN = 4
    QINGSHU = 5
    POYHU = 6
    FUZHOU = 7

class UserInfo(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    SCHOOL_ZONE = (
        (SCHOOL_ZONE_ENUM.MAIN, "主校区"),
        (SCHOOL_ZONE_ENUM.TONG_JI, "同济校区"),
        (SCHOOL_ZONE_ENUM.WANG_AN, "网安校区"),
        (SCHOOL_ZONE_ENUM.JUN_SHAN, "军山校区"),
        (SCHOOL_ZONE_ENUM.QINGSHU, "青山湖校区"),
        (SCHOOL_ZONE_ENUM.POYHU, "鄱阳湖校区"),
        (SCHOOL_ZONE_ENUM.FUZHOU, "抚州校区")
    )
    USER_TYPE = (
        (1, "普通用户"),
        (2, "管理员")
    )
    student_id = models.CharField(max_length=128, verbose_name="学号", unique=True, null=False, blank=False)
    user_name = models.CharField(max_length=64, verbose_name="用户名", null=False, blank=False)
    avatar = models.CharField(max_length=256, verbose_name="用户头像", null=True, blank=True)
    password = models.CharField(max_length=256, verbose_name="密码", null=True, blank=True)
    school_zone = models.IntegerField(choices=SCHOOL_ZONE, default=1, verbose_name="校区")
    user_type = models.IntegerField(choices=USER_TYPE, default=1, verbose_name="用户类型")
    profile = models.CharField(max_length=200, verbose_name="个人简介", null=True, blank=True)
    contact = models.CharField(max_length=64, verbose_name="联系方式", null=True, blank=True)
    email = models.CharField(max_length=128, verbose_name="邮箱", null=True, blank=True)
    uonline = models.BooleanField(default=False, verbose_name="用户是否在线")

    def __str__(self):
        return self.user_name

    def delete(self, using=None, keep_parents=False):
        # 重写delete删除模型对象同时删除图片
        name = self.avatar.split("/")[-1:]
        url = settings.STATICFILES_DIRS[0] + "/" + name[0]
        os.remove(path=url)
        super(UserInfo, self).delete()
