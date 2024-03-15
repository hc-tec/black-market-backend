from django.db import models
from .userinfoModel import UserInfo

class WeChatCertification(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "微信认证"
        verbose_name_plural = verbose_name

    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    openid = models.CharField(max_length=28, blank=False, null=False)

    def __str__(self):
        return self.user.user_name
