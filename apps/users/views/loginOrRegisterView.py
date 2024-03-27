from rest_framework.views import APIView

from django.core.cache import cache
from django.db import transaction
from apps.users.models import UserInfo

from utils import statusCode
from utils.encryption import sha256
from utils.response import validData

from utils.serializer import UserInfoSerializer
from utils.serializer import RegisterSerializer
import time


class LoginOrRegister(APIView):
    """
    用户名， 密码登录接口
    """
    authentication_classes = []

    def is_valid(self, email, ver_code):
        """
        进行邮箱验证, 先调用邮箱认证接口获取验证码
        :return:
        """
        # 判断Redis中是否存在
        assert ver_code == cache.get(email), "验证码无效"

    @validData(statusCode.LoginOrRegister)
    def post(self, request, *args, **kwargs):
        # 将数据放入字典
        user_data = dict()
        user_data["email"] = request.data["email"]
        ver_code = request.data["ver_code"]
        # 进行邮箱验证, 先调用邮箱认证接口获取验证码
        # self.is_valid(email=user_data["email"], ver_code=ver_code)
        # 判断用户是否已注册
        obj = UserInfo.objects.filter(email=user_data["email"])
        if obj:
            user_obj = obj
            assert user_obj, "邮箱错误"
            request.session['user'] = {"pk": user_obj.pk}
            ser = UserInfoSerializer(instance=user_obj, many=False)
            return ser.data
        else:
            user_data["user_name"] = "momo"
            user_data["student_id"] = str(int(time.time() * 1000))
            user_data["password"] = "WaiBiBaBuWaiBiWaiBi123@#$%^&*()"
            ser = RegisterSerializer(data=user_data)
            if ser.is_valid():
                # 数据通过验证
                # 创建图片对象
                # 添加数据库事务
                with transaction.atomic():
                    UserInfo.objects.create(**user_data)
                user_obj = UserInfo.objects.filter(**user_data).first()
                request.session['user'] = {"pk": user_obj.pk}
                ser = UserInfoSerializer(instance=user_obj, many=False)
                return ser.data
            else:
                raise Exception(ser.errors)
