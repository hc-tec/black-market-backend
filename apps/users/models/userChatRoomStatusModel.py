
from datetime import datetime

from django.db import models
from .chatRoomModel import ChatRoom
from .userinfoModel import UserInfo

from utils import functions

class UserChatRoomStatus(models.Model):

    class Meta:
        verbose_name = "用户聊天室状态"
        verbose_name_plural = verbose_name

    chat_id = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE, related_name="chatStatus", verbose_name="聊天室 ID")
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, verbose_name="用户")
    last_enter_time = models.DateTimeField(default=datetime.now(), verbose_name="上次浏览时间")

    def __str__(self):
        return "<{} [user]={} [time]={}>".format(
            self.chat_id, self.user,
            functions.format_time(self.last_enter_time)
        )
