

from datetime import datetime

from django.db import transaction

from SecondaryMarket.celery import app
from apps.chat.consumers import Chatting
from apps.users.models import (UserInfo, ChatMessage,
                               ChatRoom, UserChatRoomStatus)


def get_friend_id(user_id, chat_id: str) -> int:
    user1_id, user2_id = map(int, chat_id.split("-"))
    return user2_id if user_id == user1_id else user1_id


# @app.task
def chat_message_store(data):
    user_id = int(data["chat_user"]["id"])

    user = UserInfo.objects.filter(pk=user_id).first()
    if not user:
        return
    chat_id = data["chat_id"]
    friend_id = get_friend_id(user_id, chat_id)

    friend = UserInfo.objects.filter(pk=friend_id).first()
    if not friend:
        return

    chat_msg_type = data["chat_msg_type"]
    data["chat_msg_type"] = ChatMessage.get_chat_msg_type(chat_msg_type)
    chat_status = data["chat_status"]
    data["chat_status"] = ChatMessage.get_chat_status(chat_status)

    # 删除多余字段
    del data["chat_type"]
    del data["chat_user"]

    with transaction.atomic():
        # 创建聊天室
        chat_room, _ = ChatRoom.objects.get_or_create(chat_id=chat_id)
        # 创建用户与聊天室之间的联系

        user_chat_room, is_new = UserChatRoomStatus.objects.get_or_create(chat_id=chat_room, user=user)
        friend_chat_room, _ = UserChatRoomStatus.objects.get_or_create(chat_id=chat_room, user=friend)

        if not is_new:
            # 更新用户查看聊天室的时间
            user_chat_room.__dict__["last_enter_time"] = datetime.now()
            user_chat_room.save()

        # 由于字段为外键，将字符值重置为对象
        data["chat_id"] = chat_room
        data["user"] = user
        # 创建消息
        ChatMessage.objects.create(**data)

# 监听 聊天消息
Chatting.listen(chat_message_store)
