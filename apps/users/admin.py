from django.contrib import admin
from apps.users.models import (UserInfo, Tags, Goods, GoodsAllImage,
                     Topic, Thread, ThreadComment, ThreadImage,
                        WeChatCertification, UserChatRoomStatus,
                     ChatMessage, ChatRoom, Friend, Message,
                    GoodReport, ThreadReport, CommentReport)

models = (UserInfo, Tags, Goods, GoodsAllImage,
             Topic, Thread, ThreadComment, ThreadImage,
                WeChatCertification, UserChatRoomStatus,
             ChatMessage, ChatRoom, Friend, Message,
            GoodReport, ThreadReport, CommentReport)

for model in models:
    admin.site.register(model)
