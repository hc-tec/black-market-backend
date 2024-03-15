
from django.db import models

class ChatRoom(models.Model):

    class Meta:
        verbose_name = "聊天室"
        verbose_name_plural = verbose_name

    chat_id = models.CharField(max_length=16, primary_key=True, verbose_name="聊天室 ID")

    def __str__(self):
        return "<{}.{}>".format(self.__class__.__name__, self.chat_id)
