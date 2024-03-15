from django.db import models
from .userinfoModel import UserInfo
from .threadModel import Thread

class ThreadComment(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = '帖子评论'
        verbose_name_plural = verbose_name
        ordering = ('-comment_time',)


    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="评论用户", related_name="user_info_set")
    appreciate_user = models.ManyToManyField(UserInfo, verbose_name="点赞用户", related_name="appreciate_user_set")
    thread_info = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name="关联帖子",
                                    related_name="thread_info_set")
    comment_appreciate = models.IntegerField(default=0, verbose_name="点赞数")
    comment_parent_id = models.IntegerField(verbose_name="父评论id", null=True, blank=True)
    comment_reply_id = models.ForeignKey(UserInfo, max_length=64, verbose_name="回复用户", on_delete=models.CASCADE,
                                         null=True, blank=True)
    comment_content = models.CharField(max_length=1024, verbose_name="评论内容")
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name="帖子发布时间")

    def __str__(self):
        return self.comment_content
