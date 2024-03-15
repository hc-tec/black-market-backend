from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     DestroyAPIView, UpdateAPIView)

from apps.users.models import Goods, UserInfo
# from apps.users.models.goodsModel import Goods
from utils.pagination import (GoodsPagination, ThreadPagination)
from utils.serializer import (ThreadSerializer, GoodSerializer)


class AtomicGoodsView(ListAPIView):
    pagination_class = GoodsPagination
    serializer_class = GoodSerializer

    class Meta:
        filters = ['sold_goods', 'purchase_goods', 'current_goods', 'favor_goods']

    def get_sold_goods(self):
        return self.request.user.goods_seller_set.filter(goods_is_sold=True)

    def get_purchase_goods(self):
        return self.request.user.goods_buyer_set.all()

    def get_current_goods(self):
        return self.request.user.goods_seller_set.filter(goods_is_sold=False)

    def get_favor_goods(self):
        return self.request.user.goods_wanted_person_set.all()

    def get_queryset(self):
        filter_content = self.request.query_params.get('filter')

        if filter_content in self.Meta.filters:
            filter_func = getattr(self, f'get_{filter_content}')
            return filter_func()
        return None


class AtomicThreadView(ListAPIView):
    pagination_class = ThreadPagination
    serializer_class = ThreadSerializer

    class Meta:
        filters = ['launch_num', 'favor_num']

    def get_launch_num(self):
        return self.request.user.thread_author_info_set.all()

    def get_favor_num(self):
        return self.request.user.thread_appreciate_peoples_set.all()

    def get_queryset(self):
        filter_content = self.request.query_params.get('filter')
        if filter_content in self.Meta.filters:
            filter_func = getattr(self, f'get_{filter_content}')
            return filter_func()
        return None
