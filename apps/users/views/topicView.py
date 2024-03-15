from django.db.models import Count

from rest_framework.generics import (ListAPIView)
from utils.pagination import (TopicPagination)
from utils.serializer import (TopicSerializer, TopicHotSerializer)
from apps.users.models import Topic
from utils.HotCalculator import HotTopicSingleton
# from apps.users.models.topicModel import Topic

class TopicView(ListAPIView):

    pagination_class = TopicPagination

    def get_serializer_class(self):
        return {
            "all": TopicSerializer,
            "hot": TopicHotSerializer
        }.get(self.select, TopicSerializer)

    def get_serializer_context(self):
        return {
            'request': self.request,
            "school_zone": self.school_zone
        }

    def get_all_topic(self):
        return Topic.objects.all()

    def get_hot_topic(self):
        return HotTopicSingleton().get_all(self.school_zone)

    def get_queryset(self):
        self.select = self.request.query_params["select"]
        self.school_zone = int(
            self.request.query_params.get(
                "school_zone",
                self.request.user.school_zone
            )
        )
        handler = {
            "all": self.get_all_topic,
            "hot": self.get_hot_topic,
        }.get(self.select, self.get_all_topic)
        return handler()
        # if select == "all":
        #     return Topic.objects.all()
        # elif select == "hot":
        #     return Topic.objects.annotate(thread_num=Count("thread_topic_set")).order_by("-thread_num")
