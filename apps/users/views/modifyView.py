import re
import os



from SecondaryMarket import settings

from rest_framework.views import APIView

from django.core.cache import cache
from django.db import transaction

from apps.users.models import UserInfo
# from apps.users.models.userinfoModel import UserInfo
from utils import statusCode
from utils.encryption import sha256
from utils.response import validData


class AvatarModify(APIView):
    """
    头像修改接口
    """

    @validData(statusCode.AvatarModify)
    def put(self, request, *args, **kwargs):
        avatar = request.data["avatar"]
        user_obj = request.user
        assert user_obj, "用户不存在"
        try:
            order_avatar = user_obj.avatar
            # 添加数据库事务
            with transaction.atomic():
                # 更新头像
                user_obj.avatar = avatar
                user_obj.save()
                # 将原来的图片删除
                name = order_avatar.split("/")[-1:]
                url = settings.STATICFILES_DIRS[0] + "/" + name[0]
                os.remove(path=url)
            return {"avatar": user_obj.avatar}
        except Exception as e:
            raise Exception("更新失败")


class UserNameModify(APIView):
    """
    用户名修改接口
    """

    @validData(statusCode.UserNameModify)
    def put(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            assert user_obj, "用户不存在"
            password = request.data["password"]
            assert user_obj.password == sha256(password), "密码错误"
            user_name = request.data["user_name"]
            user_obj.user_name = user_name
            user_obj.save()
        except Exception as e:
            raise e


class StudentIdModify(APIView):
    """
    学号修改接口
    """

    @validData(statusCode.StudentIdModify)
    def put(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            assert user_obj, "用户不存在"
            password = request.data["password"]
            assert user_obj.password == sha256(password), "密码错误"
            student_id = request.data["student_id"]
            pattern = re.compile(r"^\d+$")
            assert pattern.match(student_id), "学号格式不正确"
            user_obj.student_id = student_id
            user_obj.save()
        except Exception as e:
            raise e


class SchoolZoneModify(APIView):
    """
    校区修改接口
    """

    @validData(statusCode.SchoolZoneModify)
    def put(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            assert user_obj, "用户不存在"
            password = request.data["password"]
            assert user_obj.password == sha256(password), "密码错误"
            school_zone = request.data["school_zone"]
            assert 0 < int(school_zone) <= len(UserInfo.SCHOOL_ZONE), "校区错误"
            user_obj.school_zone = school_zone
            user_obj.save()
        except Exception as e:
            raise e


class ProfileModify(APIView):
    """
    个人简介修改接口
    """

    @validData(statusCode.ProfileModify)
    def put(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            assert user_obj, "用户不存在"
            password = request.data["password"]
            assert user_obj.password == sha256(password), "密码错误"
            profile = request.data["profile"]
            user_obj.profile = profile
            user_obj.save()
        except Exception as e:
            raise e


class PasswordModify(APIView):
    """
    密码修改接口
    """

    @validData(statusCode.PasswordModify)
    def put(self, request, *args, **kwargs):
        user_data = dict()
        user_data["password"] = request.data["password"]
        # 验证密码格式
        # 密码最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符
        pattern = re.compile(r"^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*? ]).*$"r"")
        if pattern.match(user_data["password"]):
            ver_code = request.data["ver_code"]
            user_obj = request.user
            # 判断Redis中是否存在
            assert ver_code == cache.get(user_obj.pk), "验证码无效"
            try:
                user_obj.password = sha256(user_data["password"])
                user_obj.save()
            except Exception as e:
                raise Exception("密码修改失败")
            return
        else:
            raise Exception("密码错误")


class QQModify(APIView):
    """
    qq修改接口
    """

    @validData(statusCode.QQModify)
    def put(self, request, *args, **kwargs):
        user_data = dict()
        user_data["qq"] = request.data["qq"]
        # 验证qq格式
        pattern = re.compile(r"^[1-9][0-9]{4,}$")
        if pattern.match(user_data["qq"]):
            ver_code = request.data["ver_code"]
            user_obj = request.user
            # 判断Redis中是否存在
            assert ver_code == cache.get(user_obj.pk), "验证码无效"
            try:
                user_obj.qq = user_data["qq"]
                user_obj.save()
                return
            except Exception as e:
                Exception("qq修改失败")
            return
        else:
            raise Exception("qq格式错误")
