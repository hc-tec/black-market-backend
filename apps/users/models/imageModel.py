from django.db import models
from SecondaryMarket import settings
from .goodsModel import Goods
from .threadModel import Thread
import os


class GoodsAllImage(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "商品图片"
        verbose_name_plural = verbose_name

    image_path = models.CharField(max_length=256)
    product = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="关联商品")

    def __str__(self):
        return self.image_path

    def delete(self, using=None, keep_parents=False):
        # 重写delete删除模型对象同时删除图片
        name = self.image_path.split("/")[-1:]
        url = settings.STATICFILES_DIRS[0] + "/" + name[0]
        os.remove(path=url)
        super(GoodsAllImage, self).delete()

class ThreadImage(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "帖子图"
        verbose_name_plural = verbose_name

    image_path = models.CharField(max_length=256)
    post = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name="帖子图")

    def __str__(self):
        return self.image_path

    def delete(self, using=None, keep_parents=False):
        # 重写delete删除模型对象同时删除图片
        name = self.image_path.split("/")[-1:]
        url = settings.STATICFILES_DIRS[0] + "/" + name[0]
        os.remove(path=url)
        super(ThreadImage, self).delete()

