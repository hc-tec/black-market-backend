from django.db import models
from .userinfoModel import UserInfo
from .threadModel import Thread

class Message(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "消息"
        verbose_name_plural = verbose_name

    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="消息所属用户",
                               related_name="author_set")
    reply_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="消息回复的用户",
                                   related_name="reply_user_set")
    related_thread = models.ForeignKey(Thread, on_delete=models.SET_NULL, default=None, verbose_name="关联帖子",
                                       related_name="related_thread_set", null=True, blank=True)
    message_content = models.TextField(max_length=2048, verbose_name="消息内容")
    message_is_watch = models.BooleanField(verbose_name="消息是否阅读", default=False)
    message_time = models.DateTimeField(auto_now_add=True, verbose_name="消息发布时间")

    def __str__(self):
        return self.message_content

