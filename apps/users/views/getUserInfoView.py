from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     DestroyAPIView, UpdateAPIView)

from utils.serializer import UserInfoSerializer

from apps.users.models import (UserInfo)
# from apps.users.models.userinfoModel import UserInfo

class GetUserInfo(ListAPIView):
    """
    获取用户信息接口
    """
    serializer_class = UserInfoSerializer
    authentication_classes = []

    def get_queryset(self):
        id = self.request.query_params["user_id"]
        user_obj = UserInfo.objects.filter(id=id)
        return user_obj
