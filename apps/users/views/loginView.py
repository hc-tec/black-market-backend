
from rest_framework.views import APIView
from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     DestroyAPIView, UpdateAPIView)

from apps.users.models import UserInfo, WeChatCertification
# from apps.users.models.userinfoModel import UserInfo
#
# from apps.users.models.weChatCertificationModel import WeChatCertification
from utils import statusCode
from utils.encryption import sha256
from utils.response import validData
from utils.weChatApi import get_openid

from utils.serializer import UserInfoSerializer

# from models import (UserInfo, WeChatCertification)

class Login(APIView):
    """
    用户名， 密码登录接口
    """
    authentication_classes = []

    @validData(statusCode.Login)
    def post(self, request, *args, **kwargs):
        user_data = dict()
        user_data["student_id"] = request.data["student_id"]
        user_data["password"] = sha256(request.data["password"])
        user_obj = UserInfo.objects.filter(**user_data).first()
        assert user_obj, "学号或密码错误"
        request.session['user'] = {"pk": user_obj.pk}
        ser = UserInfoSerializer(instance=user_obj, many=False)
        return ser.data


class WeChatLogin(APIView):
    """
    微信登录接口
    """
    authentication_classes = []

    @validData(statusCode.WeChatLogin)
    def post(self, request, *args, **kwargs):
        # 确定用户的openid
        js_code = request.data["js_code"]
        openid = get_openid(js_code)["openid"]
        # openid = "123456"
        obj = WeChatCertification.objects.filter(openid=openid).first()
        assert obj, "用户登录失败"
        # openid存在于数据库中
        user_obj = obj.user
        # 生成session
        request.session['user'] = {"pk": user_obj.pk}
        ser = UserInfoSerializer(instance=user_obj, many=False)
        return ser.data


class AutoLogin(ListAPIView):
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        return [self.request.user]