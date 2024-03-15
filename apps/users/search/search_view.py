
import re
import requests
from datetime import datetime
from datetime import timedelta

from rest_framework.generics import (ListAPIView)

# from haystack.utils.app_loading import haystack_get_model
# from drf_haystack.viewsets import HaystackViewSet

# from apps.users.models.goodsModel import Goods
from apps.users.models import Goods, UserInfo
from utils.serializer import GoodSerializer, ChatDetailsUserInfo
from utils.pagination import GoodsPagination

class GoodsSearchView(ListAPIView):

    serializer_class = GoodSerializer
    pagination_class = GoodsPagination
    authentication_classes = []

    def get_queryset(self):
        search_words = self.request._request.GET.get("search_words")
        school_zone = self.request._request.GET.get("school_zone")

        return Goods.objects.filter(goods_title__contains=search_words, seller__school_zone=school_zone)\
            .order_by("-goods_launch_time")

    def get_serializer_context(self):
        return {
            "user": self.request.user,
        }

    def _process_results(self, raw_results: dict):

        results = []
        hit = raw_results.get("hits")
        if hit:
            hits = hit.get("hits")
            if hits:
                for hit in hits:
                    id = int(hit["_id"].split(".")[-1])
                    results.append(id)

        return results

class ChatUserSearch(ListAPIView):

    serializer_class = ChatDetailsUserInfo

    def get_queryset(self):
        search_words = self.request._request.GET.get("searchWords")
        return UserInfo.objects.filter(user_name__contains=search_words)
