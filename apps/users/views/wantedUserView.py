from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     DestroyAPIView, UpdateAPIView)

from django.db import transaction

from apps.users.models import Goods, UserInfo
# from apps.users.models.goodsModel import Goods
#
# from apps.users.models.userinfoModel import UserInfo
from utils import statusCode

from utils.response import validData

from utils.serializer import (WantedUserSerializer)
# from models import (UserInfo, Goods)


class WantedUser(ListAPIView):
    serializer_class = WantedUserSerializer

    def get_queryset(self):
        '''
        获取 [想要此商品的用户]

        根据商品 id 获取 [想要此商品的用户]
        '''
        goods_id = self.request.query_params.get('goods_id')
        goods = Goods.objects.filter(pk=goods_id).first()
        wanted_users = goods.goods_wanted_person.all()
        return wanted_users

    def is_valid(self, request):
        '''
        判断是否 商品 以及 用户 存在，
        并返回处理后的 instance
        '''
        data = request.data
        goods_id = data.get('goods_id')
        wanted_user_obj = request.user

        goods_obj = Goods.objects.filter(pk=goods_id).first()
        assert goods_obj is not None, "不存在此商品"

        assert wanted_user_obj is not None, "不存在此用户"

        return goods_obj, wanted_user_obj

    @validData(statusCode.WantedUserUpdate)
    def put(self, request, *args, **kwargs):
        '''
        更新 [想要此商品的用户]
        根据商品 id 和 用户的 id
        将此用户添加到[想要此商品的用户]中
        '''
        try:
            goods_obj, wanted_user_obj = self.is_valid(request)
            goods_obj.goods_wanted_person.add(wanted_user_obj)
        except Exception as e:
            raise e

    @validData(statusCode.WantedUserDelete)
    def delete(self, request, *args, **kwargs):
        '''
        删除 [不想要此商品的用户]
        根据商品 id 和 用户的 id
        将此用户从[想要此商品的用户]中移除
        '''
        try:
            goods_obj, not_wanted_user_obj = self.is_valid(request)
            # 添加数据库事务
            with transaction.atomic():
                # 清空
                goods_obj.goods_wanted_person.remove(not_wanted_user_obj)
        except Exception as e:
            raise e
