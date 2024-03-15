
from rest_framework.views import APIView

from django.core.cache import cache
from django.db import transaction

from apps.users.models import UserInfo, WeChatCertification
# from apps.users.models.userinfoModel import UserInfo
#
# from apps.users.models.weChatCertificationModel import WeChatCertification
from utils import statusCode
from utils.encryption import sha256
from utils.response import validData
from utils.weChatApi import get_openid

from utils.serializer import RegisterSerializer


class Register(APIView):
    """
    注册接口
    """
    authentication_classes = []

    def is_valid(self, email, ver_code):
        """
        进行邮箱验证, 先调用邮箱认证接口获取验证码
        :return:
        """
        # 判断Redis中是否存在
        assert ver_code == cache.get(email), "验证码无效"

    @validData(statusCode.Register)
    def post(self, request, *args, **kwargs):
        # 将数据放入字典
        user_data = dict()
        user_data["user_name"] = request.data["user_name"]
        user_data["student_id"] = request.data["student_id"]
        user_data["password"] = sha256(request.data["password"])
        user_data["qq"] = request.data["qq"]
        user_data["school_zone"] = request.data["school_zone"]
        user_data["profile"] = request.data["profile"]
        user_data["avatar"] = request.data["avatar"]
        ver_code = request.data["ver_code"]
        # 进行邮箱验证, 先调用邮箱认证接口获取验证码
        self.is_valid(email=user_data["qq"] + "@qq.com", ver_code=ver_code)
        # 判断用户是否已注册
        obj = UserInfo.objects.filter(student_id=user_data["student_id"], qq=user_data["qq"])
        assert not obj, "用户已注册"
        ser = RegisterSerializer(data=request.data)
        if ser.is_valid():
            # 数据通过验证
            # 创建图片对象
            # 添加数据库事务
            with transaction.atomic():
                UserInfo.objects.create(**user_data)
            return
        else:
            raise Exception(ser.errors)


class WeChatRegister(APIView):
    """
    微信注册接口
    """
    authentication_classes = []

    def is_valid(self, email, ver_code):
        """
        进行邮箱验证, 先调用邮箱认证接口获取验证码
        :return:
        """
        # 判断Redis中是否存在
        assert ver_code == cache.get(email), "验证码无效"

    @validData(statusCode.WeChatRegister)
    def post(self, request, *args, **kwargs):
        # 将数据放入字典
        user_data = dict()
        user_data["user_name"] = request.data["user_name"]
        user_data["student_id"] = request.data["student_id"]
        user_data["password"] = sha256(request.data["password"])
        user_data["qq"] = request.data["qq"]
        user_data["school_zone"] = request.data["school_zone"]
        user_data["profile"] = request.data["profile"]
        user_data["avatar"] = request.data["avatar"]
        js_code = request.data["js_code"]
        openid = get_openid(js_code)["openid"]
        ver_code = request.data["ver_code"]
        # openid = "123456"
        # 进行邮箱验证, 先调用邮箱认证接口获取验证码
        self.is_valid(email=user_data["qq"] + "@qq.com", ver_code=ver_code)
        # 判断用户是否已注册
        obj = UserInfo.objects.filter(student_id=user_data["student_id"], qq=user_data["qq"],
                                      password=user_data["password"])
        assert not obj, "用户已注册"
        ser = RegisterSerializer(data=request.data)
        if ser.is_valid():
            # 数据通过验证
            # 创建图片对象
            # 添加数据库事务
            with transaction.atomic():
                user = UserInfo.objects.create(**user_data)
                WeChatCertification.objects.create(user=user, openid=openid)
            return {"open_id": openid, "avatar": user_data["avatar"]}
        else:
            raise Exception(ser.errors)