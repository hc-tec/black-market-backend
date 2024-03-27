from rest_framework.generics import (ListAPIView)

from utils.pagination import (GoodsPagination)
from utils.serializer import (RegisterSerializer, UserInfoSerializer, ThreadSerializer, MessageSerializer,
                              GoodSerializer, WantedUserSerializer, ThreadCommentSerializer, TopicSerializer)


class GoodsSearch(ListAPIView):
    """
    根据搜索内容获取所需商品
    """
    serializer_class = GoodSerializer
    pagination_class = GoodsPagination
    authentication_classes = []

    def get_serializer_context(self):
        return {
            "user": self.request.user
        }

    def get_queryset(self):
        search_words = self.request.query_params["search_words"]
        # goods = Goods.objects.filter(goods_title__contains=search_words)
        # search_engine = SearchEngine(Goods, None)
        # results = search_engine.search("goods_title", search_words)
        # goods_ids = [goods["id"] for goods in results[0]]
        # return Goods.objects.filter(id__in=goods_ids)