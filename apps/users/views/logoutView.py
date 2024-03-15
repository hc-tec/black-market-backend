from rest_framework.views import APIView

from django.db import transaction
from utils import statusCode

from utils.response import validData


class Logout(APIView):
    """
    用户注销接口
    """

    @validData(statusCode.Logout)
    def delete(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            with transaction.atomic():
                # # 清除售卖的商品
                # user_obj.goods_seller_set.all().delete()
                # # 清除与商品表之间的关联
                # user_obj.goods_wanted_person_set.clear()
                # # 清除与话题表的关联
                # user_obj.topic_set.clear()
                # # TODO 考虑要不要删除用户发布的帖子
                # # 清除与帖子表的关联
                # user_obj.thread_appreciate_peoples_set.clear()
                # # TODO 考虑要不要删除用户发布的评论
                # # 清除与评论表的关联
                # user_obj.threadcomment_set.clear()
                # # 清除与微信认证表的关联
                # user_obj.WeChatCertification.delete()
                # 删除用户数据
                request.session.flush()
                user_obj.delete()
            return
        except Exception as e:
            raise e
