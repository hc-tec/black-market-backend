import os

from django.db import models
from SecondaryMarket import settings
from .userinfoModel import UserInfo
from .tagsModel import Tags

class AUDIT_STATUS_ENUM:
    AUDITING = 3000
    AUDIT_PASS = 3001
    AUDIT_DENY = 3002

class GOOD_TYPE_ENUM:
    PHONE = 1
    MAN_CLOSE = 2
    WOMAN_CLOSE = 3
    DIGIT = 4
    SPORT = 5
    TOILETRY = 6
    FOOD = 7
    PACKAGE = 8
    SHOE = 9
    ORNAMENT = 10
    ELECTRIC = 11
    MEDICINE = 12
    BOOK = 13
    STATIONERY = 14
    OTHERS = 15

class GOOD_AREA_ENUM:
    NORMAL_AREA = 1
    SPECIAL_AREA = 2
    FREE_AREA = 3

class Goods(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    AUDIT_STATUS = (
        (AUDIT_STATUS_ENUM.AUDITING, "等待管理员审核"),
        (AUDIT_STATUS_ENUM.AUDIT_PASS, "审核通过"),
        (AUDIT_STATUS_ENUM.AUDIT_DENY, "审核未通过"),
    )
    GOOD_TYPE = (
        (GOOD_TYPE_ENUM.PHONE, "手机"),
        (GOOD_TYPE_ENUM.MAN_CLOSE, "男装"),
        (GOOD_TYPE_ENUM.WOMAN_CLOSE, "女装"),
        (GOOD_TYPE_ENUM.DIGIT, "数码"),
        (GOOD_TYPE_ENUM.SPORT, "运动"),
        (GOOD_TYPE_ENUM.TOILETRY, "洗护"),
        (GOOD_TYPE_ENUM.FOOD, "食品"),
        (GOOD_TYPE_ENUM.PACKAGE, "箱包"),
        (GOOD_TYPE_ENUM.SHOE, "鞋靴"),
        (GOOD_TYPE_ENUM.ORNAMENT, "饰品"),
        (GOOD_TYPE_ENUM.ELECTRIC, "电器"),
        (GOOD_TYPE_ENUM.MEDICINE, "医药"),
        (GOOD_TYPE_ENUM.BOOK, "书籍"),
        (GOOD_TYPE_ENUM.STATIONERY, "文具"),
        (GOOD_TYPE_ENUM.OTHERS, "其它"),
    )
    GOOD_AREA = (
        (GOOD_AREA_ENUM.NORMAL_AREA, "普通分区"),
        (GOOD_AREA_ENUM.SPECIAL_AREA, "特价分区"),
        (GOOD_AREA_ENUM.FREE_AREA, "免费分区"),
    )
    seller = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="卖家", related_name="goods_seller_set")
    goods_title = models.CharField(max_length=128, verbose_name="商品标题")
    goods_price = models.DecimalField(decimal_places=2, max_digits=32, verbose_name="商品价格")
    goods_main_image = models.CharField(max_length=256, null=True, blank=True, verbose_name="商品主图")
    goods_desc = models.TextField(max_length=1000, verbose_name="商品描述")
    goods_launch_time = models.DateTimeField(auto_now_add=True, verbose_name="商品上架时间")
    goods_area = models.IntegerField(choices=GOOD_AREA, default=GOOD_AREA_ENUM.NORMAL_AREA, verbose_name="商品分区")
    goods_is_sold = models.BooleanField(verbose_name="是否已卖出", default=False)
    goods_type = models.IntegerField(choices=GOOD_TYPE, default=GOOD_TYPE_ENUM.OTHERS, verbose_name="商品类别")
    buyer = models.ManyToManyField(UserInfo, related_name="goods_buyer_set", verbose_name="买家")
    goods_wanted_person = models.ManyToManyField(UserInfo, related_name="goods_wanted_person_set", verbose_name="想要的用户")
    goods_tags = models.ManyToManyField(Tags, related_name="goods_tags_set", verbose_name="商品标签")
    flag = models.IntegerField(choices=AUDIT_STATUS, default=AUDIT_STATUS_ENUM.AUDITING, verbose_name="商品是否审核")

    def __str__(self):
        return self.goods_title

    def delete(self, using=None, keep_parents=False):
        # 重写delete删除模型对象同时删除图片
        name = self.goods_main_image.split("/")[-1:]
        url = settings.STATICFILES_DIRS[0] + "/" + name[0]
        os.remove(path=url)
        super(Goods, self).delete()
