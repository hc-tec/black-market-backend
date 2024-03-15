from django.db import models
from .userinfoModel import UserInfo

class Topic(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "话题"
        verbose_name_plural = verbose_name

    topic_focus = models.ManyToManyField(UserInfo, related_name="topic_focus_set", verbose_name="关注用户")
    topic_content = models.CharField(max_length=128, verbose_name="话题")

    def __str__(self):
        return self.topic_content
