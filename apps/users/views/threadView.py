from django.db import transaction
from rest_framework.generics import ListAPIView

from apps.users.models import (Thread, UserInfo,
                               Topic, ThreadImage,
                               AUDIT_STATUS_ENUM)
# from apps.users.models.userinfoModel import UserInfo
# from apps.users.models.threadModel import Thread
# from apps.users.models.topicModel import Topic
# from apps.users.models.imageModel import ThreadImage

from utils import statusCode
from utils.HotCalculator import HotTopicThreadSingleton, HotThreadSingleton
from utils.pagination import ThreadPagination
from utils.response import validData
from utils.serializer import ThreadSerializer


class ThreadView(ListAPIView):
    """
    下面三行代码用于帖子的获取
    """
    authentication_classes = []
    pagination_class = ThreadPagination
    serializer_class = ThreadSerializer

    def get_filter_goods(self, includes: list):
        return Thread.objects.filter(**{
            key: val for key, val in self.filters.items() if key in includes
        }).order_by("-thread_time")

    def get_queryset(self):

        data = self.request.query_params
        display_type = data.get("display_type")
        self.filters = {
            "thread_topic__topic_content": data.get('topic'),
            "author_info_id": data.get("user_id"),
            "author_info__school_zone": int(data.get("school_zone", 1)),
            "flag": int(data.get("audit_status", AUDIT_STATUS_ENUM.AUDIT_PASS))
        }
        # 热榜形式
        if display_type == "hot":
            # 某个话题下的热榜
            if self.filters["thread_topic__topic_content"]:
                topic = Topic.objects.filter(
                    topic_content=self.filters["thread_topic__topic_content"]
                ).first()
                assert topic, "话题不存在"
                return HotTopicThreadSingleton().get_all(
                    topic,
                    self.filters["author_info__school_zone"]
                )
            # 所有帖子下的热榜
            return HotThreadSingleton().get_all(
                self.filters["author_info__school_zone"]
            )


        if self.filters["thread_topic__topic_content"]:
            # 时间排序形式
            return self.get_filter_goods(
                ["flag", "author_info__school_zone", "thread_topic__topic_content"]
            )
        if self.filters["author_info_id"]:
            return self.get_filter_goods(["flag", "author_info_id"])
        return self.get_filter_goods(["flag", "author_info__school_zone"])
        # topic = self.request.query_params.get('topic')
        # user_id = self.request.query_params.get("user_id")
        # school_zone = self.request.query_params.get('school_zone') or 1
        # if topic:
        #     return Thread.objects.filter(thread_topic__topic_content=topic,
        #                                  author_info__school_zone=school_zone)\
        #         .order_by("-thread_time")
        # elif user_id:
        #     return Thread.objects.filter(author_info_id=user_id).all()
        # return Thread.objects.filter(author_info__school_zone=school_zone).order_by("-thread_time")

    @validData(statusCode.ThreadUpload)
    def post(self, request, *args, **kwargs):
        """
        发布新的帖子
        """
        try:
            thread_data = dict()
            # 获取前端发来的信息
            thread_data["user_id"] = request.data["user_id"]
            thread_data["thread_topic"] = request.data["thread_topic"]
            thread_data["thread_images"] = request.data["thread_images"]
            thread_data["thread_info"] = request.data["thread_info"]
            # 添加数据库事务
            with transaction.atomic():
                # 保存帖子标题
                topic = Topic.objects.get_or_create(topic_content=thread_data["thread_topic"])
                # 创建帖子
                thread_obj = Thread.objects.create(
                    author_info=UserInfo.objects.filter(id=thread_data["user_id"]).first(),
                    thread_info=thread_data["thread_info"], thread_topic=topic[0])
                # 保存图片并与帖子建立关联
                for image in thread_data["thread_images"]:
                    ThreadImage.objects.create(image_path=image, post=thread_obj)
            return
        except Exception as e:
            raise e

    @validData(statusCode.ThreadDelete)
    def delete(self, request, *args, **kwargs):
        """
        根据帖子id删除帖子
        """
        try:
            thread_id = request.data["thread_id"]
            thread_obj = Thread.objects.filter(id=thread_id).first()
            with transaction.atomic():
                thread_obj.delete()
            return
        except Exception as e:
            raise e
