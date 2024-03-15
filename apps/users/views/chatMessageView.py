

from rest_framework.generics import (ListAPIView)

from utils import serializer

from apps.users.models import ChatRoom, ChatMessage as ChatMessageModel

class ChatMessage(ListAPIView):

    serializer_class = serializer.ChatMessageSerializer

    def get_queryset(self):

        user = self.request.user
        chat_id = self.request._request.GET.get("chat_id")

        chat_room = ChatRoom.objects.filter(pk=chat_id).first()

        assert chat_room, "聊天室不存在"

        self.has_permission(user, chat_room)

        return ChatMessageModel.objects.filter(
            chat_id=chat_room)

    def has_permission(self, user, chat_room):
        assert str(user.id) in chat_room.chat_id.split("-"), {
            "status": "用户没有权限"
        }
