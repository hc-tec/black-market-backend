
from django.db import models

from .chatRoomModel import ChatRoom
from .userinfoModel import UserInfo

from utils import functions

class CHAT_MSG_STATUS:
    SUCCESS = 1
    FAIL = 2

class CHAT_MSG_TYPE:
    TEXT = 1
    IMG = 2

class ChatMessage(models.Model):

    class Meta:
        verbose_name = "聊天消息"
        verbose_name_plural = verbose_name

    CHAT_MESSAGE_TYPE = (
        (CHAT_MSG_TYPE.TEXT, "text"),
        (CHAT_MSG_TYPE.IMG, "img")
    )
    CHAT_MESSAGE_TYPE_MAP = {
        "text": CHAT_MSG_TYPE.TEXT,
        "img": CHAT_MSG_TYPE.IMG
    }
    CHAT_MESSAGE_STATUS = (
        (CHAT_MSG_STATUS.SUCCESS, "success"),
        (CHAT_MSG_STATUS.FAIL, "fail")
    )
    CHAT_MESSAGE_STATUS_MAP = {
        "success": CHAT_MSG_STATUS.SUCCESS,
        "fail": CHAT_MSG_STATUS.FAIL
    }
    chat_id = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE, related_name="message", verbose_name="所属聊天室")
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, verbose_name="消息发送人")
    chat_msg_type = models.SmallIntegerField(choices=CHAT_MESSAGE_TYPE, default=1, verbose_name="消息类型")
    chat_status = models.SmallIntegerField(choices=CHAT_MESSAGE_STATUS, default=1, verbose_name="消息状态")
    chat_msg = models.CharField(max_length=1024, verbose_name="消息内容")
    # 交由消息队列处理，可能会有延迟，因此时间手动设置，不设置自动处理
    chat_time = models.DateTimeField(verbose_name="消息发送时间")

    def __str__(self):
        status = self.CHAT_MESSAGE_STATUS[self.chat_msg_type-1][1]
        return "<{}.{}.{} [type]={} [time]={}>".format(
            self.__class__.__name__, self.chat_id, self.user,
            status, functions.format_time(self.chat_time),
        )

    @staticmethod
    def get_chat_msg_type(chat_msg_type: str):
        return ChatMessage.CHAT_MESSAGE_TYPE_MAP.get(
            chat_msg_type, CHAT_MSG_TYPE.TEXT)

    @staticmethod
    def get_chat_status(chat_status: str):
        return ChatMessage.CHAT_MESSAGE_STATUS_MAP.get(
            chat_status, CHAT_MSG_STATUS.SUCCESS)
