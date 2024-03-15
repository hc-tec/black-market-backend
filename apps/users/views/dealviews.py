from rest_framework.views import APIView

from django.db import transaction

# from apps.users.models.goodsModel import Goods
#
# from apps.users.models.userinfoModel import UserInfo
from utils import statusCode
from utils.response import validData

from apps.users.models import (UserInfo, Goods)

class DealView(APIView):

    @validData(statusCode.GoodSold)
    def post(self, request, *args, **kwargs):
        """
        根据 用户id + 卖出商品id 从想要的用户中挑选出买家
        """
        try:
            user_obj = request.user
            goods = user_obj.goods_seller_set.all()
            buyer_id = request.data["buyer_id"]
            goods_id = request.data["goods_id"]
            goods_obj = Goods.objects.filter(id=goods_id).first()
            assert goods_obj in goods, "没有卖出权限"
            assert goods_obj, "卖出商品不存在"
            assert not goods_obj.goods_is_sold, "商品已买出"
            wanted_users = goods_obj.goods_wanted_person.all()
            buyer_obj = UserInfo.objects.filter(id=buyer_id).first()
            assert buyer_obj, "买家不存在"
            if buyer_obj in wanted_users:
                with transaction.atomic():
                    goods_obj.buyer.add(buyer_obj)
                    # 设置商品为已卖出
                    goods_obj.goods_is_sold = True
                    goods_obj.save()
            else:
                raise Exception("买家不在想要用户之列")
        except Exception as e:
            raise e
