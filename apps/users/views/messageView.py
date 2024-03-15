from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     DestroyAPIView, UpdateAPIView)
from django.db import transaction
from utils import statusCode
from utils.response import validData
from utils.serializer import (RegisterSerializer, UserInfoSerializer, ThreadSerializer, MessageSerializer,
                              GoodSerializer, WantedUserSerializer, ThreadCommentSerializer, TopicSerializer)
from apps.users.models import (Message)
# from apps.users.models.messageModel import Message
class MessageView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        默认获取当前用户的所有消息
        1.根据用户id获取用户的消息
        2.根据消息id获取消息
        3.根据用户id+ is_watch=True获取用户已读消息
        4.根据用户id+ is_watch=False获取用户未读消息
        """
        user_id = self.request.query_params.get("user_id", None)
        message_id = self.request.query_params.get("message_id", None)
        is_watch = self.request.query_params.get("is_watch", None)
        if user_id and is_watch:
            return Message.objects.filter(reply_user_id=user_id, message_is_watch=is_watch)
        elif message_id:
            message_obj = Message.objects.filter(id=message_id)
            for obj in message_obj:
                obj.message_is_watch = True
                obj.save()
            return message_obj
        elif user_id:
            return Message.objects.filter(reply_user_id=user_id)
        else:
            return Message.objects.filter(reply_user=self.request.user)

    @validData(statusCode.MessageDelete)
    def delete(self, request, *args, **kwargs):
        """
        根据消息id批量删除消息
        """
        try:
            messages_id = list()
            messages_id = request.data.get("messages_id", None)
            with transaction.atomic():
                for message_id in messages_id:
                    message_obj = Message.objects.filter(id=message_id).first()
                    # 判断消息是否存在
                    assert message_obj, "消息不存在"
                    # 判断消息是否属于当前用户
                    assert message_obj.author == request.user, "无删除权限"
                    message_obj.delete()
            return
        except Exception as e:
            raise e