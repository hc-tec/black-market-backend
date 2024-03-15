from django.db import models
from .userinfoModel import UserInfo
from .topicModel import Topic

class AUDIT_STATUS_ENUM:
    AUDITING = 3000
    AUDIT_PASS = 3001
    AUDIT_DENY = 3002

class Thread(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "帖子"
        verbose_name_plural = verbose_name

    AUDIT_STATUS = (
        (AUDIT_STATUS_ENUM.AUDITING, "等待管理员审核"),
        (AUDIT_STATUS_ENUM.AUDIT_PASS, "审核通过"),
        (AUDIT_STATUS_ENUM.AUDIT_DENY, "审核未通过"),
    )
    author_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户信息",
                                    related_name="thread_author_info_set")
    thread_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="所属话题",
                                     related_name="thread_topic_set")
    thread_info = models.TextField(max_length=2000, verbose_name="帖子内容")
    thread_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    thread_appreciate = models.IntegerField(verbose_name="点赞数", default=0)
    thread_appreciate_peoples = models.ManyToManyField(UserInfo, verbose_name="点赞人员",
                                                       related_name="thread_appreciate_peoples_set")
    flag = models.IntegerField(choices=AUDIT_STATUS, default=3000, verbose_name="帖子是否审核")

    def __str__(self):
        return self.thread_topic.topic_content
