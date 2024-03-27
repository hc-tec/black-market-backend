import re
from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, fields

from apps.users.models import *
from utils.HotCalculator import HotTopicThreadSingleton
from . import functions

# from apps.users.models.userinfoModel import UserInfo
# from apps.users.models.threadModel import Thread
# from apps.users.models.topicModel import Topic
# from apps.users.models.messageModel import Message
# from apps.users.models.goodsModel import Goods
# from apps.users.models.threadCommentModel import ThreadComment
# from apps.users.models.imageModel import ThreadImage


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["student_id", "user_name", "password",
                  "school_zone", "profile", "email"]
        extra_kwargs = {
            "email": {"required": True}
        }

    def validate_student_id(self, value):
        pattern = re.compile(r"^\d+$")
        if pattern.match(value):
            return value
        else:
            raise serializers.ValidationError("学号格式不正确")

    def validate_password(self, value):
        # 密码最少6位，1个小写字母，1个数字，1个特殊字符
        pattern = re.compile(r"^.*(?=.{6,})(?=.*\d)(?=.*[a-z])(?=.*[~!@#$%^&*? ]).*$"r"")
        if pattern.match(value):
            return value
        else:
            raise serializers.ValidationError("密码最少6位，包括至少1个小写字母，1个数字，1个特殊字符(~!@#$%^&*? )")

    def validate_school_zone(self, value):
        if 0 > value or value > len(UserInfo.SCHOOL_ZONE):
            raise serializers.ValidationError("选项不合法")
        return value

    def validate_email(self, value):
        pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if pattern.match(value):
            return value
        else:
            raise serializers.ValidationError("邮箱格式不正确")


class UserInfoSerializer(ModelSerializer):
    txn_statistics = serializers.SerializerMethodField()
    commuca_statistics = serializers.SerializerMethodField()
    school_zone = serializers.CharField(source="get_school_zone_display")
    user_type = serializers.CharField(source="get_user_type_display")
    message_num = serializers.SerializerMethodField()  # 用户未读消息的数量

    class Meta:
        model = UserInfo
        fields = ["id", "student_id", "user_name", "avatar",
                  "school_zone", "user_type", "profile", "email", "message_num", "txn_statistics",
                  "commuca_statistics"]

    def get_message_num(self, row):
        return Message.objects.filter(reply_user=row, message_is_watch=False).count()

    def get_txn_statistics(self, row):
        result = dict()
        result["sold_goods"] = row.goods_seller_set.filter(goods_is_sold=True).count()  # 售卖量
        result["purchase_goods"] = Goods.objects.filter(goods_is_sold=True, buyer=row).count()  # 购买量
        result["current_goods"] = row.goods_seller_set.filter(goods_is_sold=False, flag=True).count()  # 当前上架数量
        result["unaudited_goods"] = row.goods_seller_set.filter(flag=False).count()  # 未审核商品数量
        result["favor_goods"] = row.goods_wanted_person_set.all().count()  # 成功交易量
        return result

    def get_commuca_statistics(self, row):
        result = dict()
        # result["focus_topics"] = row.thread_appreciate_peoples_set.all().count()  # 关注帖子数量
        result["launch_num"] = row.thread_author_info_set.all().count()  # 发表帖子数量
        result["favor_num"] = row.thread_appreciate_peoples_set.all().count()  # 点赞帖子数量
        return result


class GoodSerializer(ModelSerializer):
    seller = serializers.SerializerMethodField()
    goodsInfo = serializers.SerializerMethodField()

    def __init__(self, instance=None, user=None, data=fields.empty, **kwargs):
        self.user = user or kwargs["context"].get("user")
        super().__init__(instance, data=data, **kwargs)

    class Meta:
        model = Goods
        fields = ["seller", "goodsInfo"]

    def get_seller(self, row):
        result = dict()
        result["id"] = row.seller.id
        result["user_name"] = row.seller.user_name
        result["school_zone"] = row.seller.get_school_zone_display()
        result["avatar"] = row.seller.avatar
        result["email"] = row.seller.email
        return result

    def get_goodsInfo(self, row):
        result = dict()
        result["goods_id"] = row.id
        result["goods_main_image"] = row.goods_main_image
        # 拿到商品图片
        images = row.goodsallimage_set.all()
        result["goods_img"] = list()
        for img in images:
            result["goods_img"].append(img.image_path)
        result["goods_title"] = row.goods_title
        result["goods_price"] = row.goods_price
        # 拿到商品标签
        tags = row.goods_tags.all()
        result["goods_tags"] = list()
        for tag in tags:
            result["goods_tags"].append(tag.tags_content)
        result["goods_desc"] = row.goods_desc
        result["goods_launch_time"] = row.goods_launch_time.strftime("%Y-%m-%d %H:%M:%S")
        result["goods_is_sold"] = row.goods_is_sold
        if result["goods_is_sold"]:
            result["goods_sold_user"] = row.buyer.first().id
        # 拿到商品想要人的数量
        result["goods_wanted_person"] = row.goods_wanted_person.all().count()
        result["is_wanted_user"] = self.user in row.goods_wanted_person.all()
        result["flag"] = row.get_flag_display()
        result["goods_type"] = row.get_goods_type_display()
        return result


class WantedUserSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["id", "student_id", "user_name", "avatar"]


class ThreadSerializer(ModelSerializer):

    author_info = serializers.SerializerMethodField()
    thread_isAppreciate = serializers.SerializerMethodField()
    thread_appreciate_peoples = serializers.SerializerMethodField()
    thread_images = serializers.SerializerMethodField()
    comment_num = serializers.SerializerMethodField()
    thread_topic = serializers.CharField(source='thread_topic.topic_content')
    thread_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    flag = serializers.CharField(source="get_flag_display")

    def get_comment_num(self, row):
        return len(ThreadComment.objects.filter(thread_info=row))

    def get_author_info(self, row):
        author = row.author_info
        return {
            "id": author.id,
            "user_name": author.user_name,
            "school_zone": author.get_school_zone_display(),
            "avatar": author.avatar
        }

    def get_thread_isAppreciate(self, row):
        appreciate_users = row.thread_appreciate_peoples.all()
        return self.context["request"].user in appreciate_users

    def get_thread_appreciate_peoples(self, row):
        appreciate_users = row.thread_appreciate_peoples.all()
        return [
            user.user_name for user in appreciate_users
        ]

    def get_thread_images(self, row):
        images = ThreadImage.objects.filter(post=row)
        return [
            img.image_path for img in images
        ]

    class Meta:
        model = Thread
        fields = ["id", "author_info", "thread_topic", "thread_info",
                  "thread_time", "thread_appreciate", "thread_isAppreciate",
                  "thread_appreciate_peoples", "thread_images", "comment_num", "flag"]


class ThreadCommentSerializer(ModelSerializer):
    thread_id = serializers.CharField(source='thread_info.id')
    comment_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    comment_reply_name = serializers.SerializerMethodField()
    comment_id = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    comment_appreciate = serializers.SerializerMethodField()
    comment_isAppreciate = serializers.SerializerMethodField()
    comment_children = serializers.SerializerMethodField()

    def __init__(self, instance=None, user=None, data=fields.empty, **kwargs):
        self.user = user or kwargs["context"].get("user")
        super().__init__(instance, data=data, **kwargs)

    class Meta:
        model = ThreadComment

        fields = ["comment_id", "user_info", "thread_id",
                  "comment_appreciate", "comment_parent_id",
                  "comment_reply_name", "comment_content",
                  "comment_time", "comment_isAppreciate",
                  "comment_children"]

    def get_comment_reply_name(self, row):
        return row.comment_reply_id.user_name \
                    if row.comment_reply_id and row.user_info.id != row.comment_parent_id else \
                None

    def get_comment_id(self, row):
        return row.id

    def get_user_info(self, row):
        author = row.user_info
        return {
            "id": author.id,
            "user_name": author.user_name,
            "school_zone": author.get_school_zone_display(),
            "avatar": author.avatar
        }

    def get_comment_appreciate(self, row):
        return len(row.appreciate_user.all())

    def get_comment_isAppreciate(self, row):
        appreciate_users = row.appreciate_user.all()
        return self.user in appreciate_users

    def get_comment_children(self, row):
        if row.comment_parent_id:
            return []
        comment_children = ThreadComment.objects.filter(
            thread_info=row.thread_info,
            comment_parent_id=row.id
        )
        ser = ThreadCommentSerializer(comment_children, user=self.user, many=True)
        return ser.data


class TopicSerializer(ModelSerializer):
    topic_focus_num = serializers.SerializerMethodField()
    thread_num = serializers.SerializerMethodField()
    topic_focus_num_school_zone = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["topic_focus_num", "thread_num", "topic_content",
                  "topic_focus_num_school_zone"]

    def get_topic_focus_num_school_zone(self, row):
        return row.topic_focus.filter(
            school_zone=self.context["school_zone"]
        ).count()

    def get_topic_focus_num(self, row):
        return row.topic_focus.all().count()

    def get_thread_num(self, row):
        return row.thread_topic_set.filter(
            flag=AUDIT_STATUS_ENUM.AUDIT_PASS,
            author_info__school_zone=self.context["school_zone"],
        ).count()

class TopicHotSerializer(TopicSerializer):

    class Meta:
        model = Topic
        fields = ["topic_focus_num", "thread_num", "topic_content",
                  "hot_thread", "topic_focus_num_school_zone"]

    hot_thread = serializers.SerializerMethodField()

    def get_hot_thread(self, row):
        hot_thread = HotTopicThreadSingleton().get_first(row, self.context["school_zone"])
        return ThreadSerializer(instance=hot_thread, context=self.context).data \
                if hot_thread else \
                None

class MessageSerializer(ModelSerializer):
    author = serializers.SerializerMethodField()
    # thread_topic = serializers.SerializerMethodField()
    message_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Message
        fields = ["author", "related_thread", "message_content", "message_is_watch", "message_time"]

    def get_author(self, row):
        author = row.author
        return {
            "id": author.id,
            "user_name": author.user_name
        }

    # def get_thread_topic(self, row):
    #     thread_obj = row.related_thread
    #     return thread_obj.thread_topic.topic_content

class ChatUserInfo(ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ["id", "user_name", "avatar", "uonline"]

class ChatDetailsUserInfo(UserInfoSerializer):

    class Meta:
        model = UserInfo
        fields = ["id", "student_id", "user_name", "avatar",
                  "school_zone", "profile", "uonline"]

class FriendSerializer(ModelSerializer):

    # friend_status = serializers.CharField(source="get_friend_status_display")

    class Meta:
        model = Friend
        fields = ["friend", "message", "friend_status"]

    friend = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    def get_friend(self, row):
        if self.context["role"] == "own":
            return ChatUserInfo(instance=row.friend_id).data
        else:
            return ChatUserInfo(instance=row.own_id).data

    def get_message(self, row):
        ret = {}
        user = row.own_id
        friend = row.friend_id
        # 获取聊天室
        chat_id = functions.generate_chat_id(user.id, friend.id)
        chat_room, is_new = ChatRoom.objects.get_or_create(pk=chat_id)
        if is_new:
            UserChatRoomStatus.objects.create(chat_id=chat_room, user=user)
            UserChatRoomStatus.objects.create(chat_id=chat_room, user=friend)
        # 获取用户上一次浏览聊天室时间，以计算未读消息数量
        chat_room_status = chat_room.chatStatus.filter(user=user).first()
        last_enter_time = chat_room_status.last_enter_time
        # 筛选未读消息
        unread_message = chat_room.message.filter(
            chat_time__gt=last_enter_time).order_by("-chat_time")
        unread_count = unread_message.count()
        ret["unread_num"] = unread_count
        # 最新消息
        newest_message = chat_room.message.last()
        if newest_message:
            ret["newest_message"] = newest_message.chat_msg
            ret["newest_time"] = newest_message.chat_time
            ret["sender"] = newest_message.user.id

        return ret


class ChatMessageSerializer(ModelSerializer):

    chat_type = serializers.SerializerMethodField()
    chat_status = serializers.CharField(source="get_chat_status_display")
    chat_msg_type = serializers.CharField(source="get_chat_msg_type_display")

    def get_chat_type(self, row):
        return "chat"

    class Meta:
        model = ChatMessage
        fields = ["chat_type", "chat_status", "chat_msg",
                  "chat_msg_type", "chat_time", "chat_user"]

    chat_user = serializers.SerializerMethodField()

    def get_chat_user(self, row):
        return ChatUserInfo(instance=row.user).data
