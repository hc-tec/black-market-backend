import os

from SecondaryMarket import settings

from rest_framework.generics import (ListAPIView)

from django.db import transaction

from apps.users.models import (Goods, GoodsAllImage, Tags,
                                UserInfo, AUDIT_STATUS_ENUM,
                               GOOD_AREA_ENUM, GOOD_TYPE_ENUM)

from utils import statusCode
from utils.response import validData
from utils.pagination import (GoodsPagination)
from utils.serializer import GoodSerializer


class GoodsView(ListAPIView):
    """
        获取 所有商品 | 某一用户售买的商品
    """
    authentication_classes = []
    pagination_class = GoodsPagination
    serializer_class = GoodSerializer

    def get_serializer_context(self):
        return {
            "user": self.request.user
        }

    def get_filter_goods(self, includes: list):
        return Goods.objects.filter(**{
            key: val for key, val in self.filters.items() if key in includes
        }).order_by("-goods_launch_time")

    def get_queryset(self):
        data = self.request.query_params
        self.filters = {
            "seller": data.get('user_id', None),
            "seller__school_zone": int(data.get('school_zone', 1)),
            "goods_area": data.get("goods_area", None),
            "goods_type": data.get("goods_type", None),
            "goods_is_sold": bool(data.get("is_sold")),
            "flag": data.get("audit_status", AUDIT_STATUS_ENUM.AUDIT_PASS),
        }

        if self.filters["seller"]:
            self.filters["seller"] = UserInfo.objects.filter(pk=self.filters["seller"]).first()
            assert self.filters["seller"], "用户不存在"
            return self.get_filter_goods(
                ["seller", "goods_is_sold"]
                    if self.filters["goods_is_sold"] else \
                ["seller", "goods_is_sold", "flag"]
            )

        if self.filters["goods_area"]:
            self.filters["goods_is_sold"] = False
            return self.get_filter_goods(
                ["flag", "seller__school_zone", "goods_area", "goods_is_sold"]
            )
        if self.filters["goods_type"]:
            self.filters["goods_is_sold"] = False
            return self.get_filter_goods(
                ["flag", "seller__school_zone", "goods_type", "goods_is_sold"]
            )
        return self.get_filter_goods(
            ["flag", "seller__school_zone", "goods_is_sold"]
        )
        # goods = Goods.objects.filter(flag=audit_status) \
        #             if not is_sold else \
        #         Goods.objects.all()
        # # 根据商品类型筛选
        # goods_type = data.get("goods_type", None)
        # if goods_type:
        #     return goods.filter(goods_type=goods_type, seller__school_zone=school_zone)\
        #                 .order_by("-goods_launch_time")
        # if user_id:
        #     # 返回某一用户售卖且已经审核通过的商品
        #     user_id = UserInfo.objects.filter(pk=user_id).first()
        #     assert user_id, "用户不存在"
        #     return goods.filter(seller=user_id, goods_is_sold=is_sold)\
        #         .order_by("-goods_launch_time")
        # # 返回未正在售卖且已经审核通过的商品
        # return goods.filter(goods_is_sold=is_sold, seller__school_zone=school_zone).order_by(
        #     "-goods_launch_time")


class GoodsUploadAndUpdateView(ListAPIView):
    """
        上传更新所提供商品
    """
    pagination_class = GoodsPagination
    serializer_class = GoodSerializer

    @validData(statusCode.GoodUpload)
    def post(self, request, *args, **kwargs):
        """
            商品上传接口
        """
        try:
            good_data = dict()
            good_data["seller"] = request.user
            good_data["goods_main_image"] = request.data["goods_main_image"]
            good_data["goods_title"] = request.data["goods_title"]
            good_data["goods_price"] = request.data["goods_price"]
            good_data["goods_desc"] = request.data["goods_desc"]
            # good_data["goods_area"] = request.data.get("goods_area", GOOD_AREA_ENUM.NORMAL_AREA)
            good_data["goods_type"] = request.data.get("goods_type", GOOD_TYPE_ENUM.OTHERS)
            goods_img = request.data["goods_img"]
            # 添加数据库事务
            with transaction.atomic():
                good = Goods.objects.create(**good_data)
                # 保存商品图片，并与商品建立关联
                for img in goods_img:
                    GoodsAllImage.objects.create(image_path=img, product=good)
                # 商品标签与商品建立关联
                goods_tags = request.data["goods_tags"]
                tags = list()
                for tag in goods_tags:
                    tag_obj = Tags.objects.update_or_create(tags_content=tag, defaults={"tags_content": tag})
                    tags.append(tag_obj[0].pk)
                good.goods_tags.add(*tags)
                good.save()
            ser = GoodSerializer(instance=good, user=request.user, many=False)
            return ser.data
        except Exception as e:
            return e

    @validData(statusCode.GoodsModify)
    def put(self, request, *args, **kwargs):
        """
            修改商品信息
        """
        try:
            id = request.data["id"]
            good = Goods.objects.get(id=id)
            assert good.seller.id == request.user.pk, "没有修改权限"
            good.goods_title = request.data["goods_title"]
            good.goods_price = request.data["goods_price"]
            good.goods_desc = request.data["goods_desc"]
            # 添加数据库事务
            with transaction.atomic():
                order_main_image = good.goods_main_image
                # 添加新主图
                good.goods_main_image = request.data["goods_main_image"]
                # 删除原有主图
                if order_main_image != "":
                    name = order_main_image.split("/")[-1:]
                    url = settings.STATICFILES_DIRS[0] + "/" + name[0]
                    os.remove(path=url)
                # 删除原有图片
                images = GoodsAllImage.objects.filter(product=id)
                for image in images:
                    image.delete()
                # 添加新图片
                goods_img = request.data["goods_img"]
                # 保存商品图片，并与商品建立关联
                for img in goods_img:
                    GoodsAllImage.objects.create(image_path=img, product=good)
                # 商品标签与商品建立关联
                new_tags = request.data["goods_tags"]
                tags = list()
                # 取出商品原有标签
                goods_tags = good.goods_tags.all()
                # 删除原有标签
                for tag in goods_tags:
                    tag.delete()
                # 添加新标签
                for tag in new_tags:
                    tags.append(Tags.objects.update_or_create(tags_content=tag, defaults={"tags_content": tag})[0].pk)
                # 商品与新标签建立关联
                good.goods_tags.add(*tags)
                # 保存商品
                good.save()
            ser = GoodSerializer(instance=good, user=request.user, many=False)
            return ser.data
        except Exception as e:
            raise e

