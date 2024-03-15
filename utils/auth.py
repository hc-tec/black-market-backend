from rest_framework import authentication
from rest_framework import exceptions
from apps.users.models import UserInfo


# class MyTokenAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         token = request.query_params["token"]
#         token_obj = Token.objects.filter(user_token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed("用户认证失败")
#         return token_obj.user, token_obj

class MySessionAuthentication(authentication.BaseAuthentication):
    """验证用户是否登录"""

    def authenticate(self, request):

        user_data = request.session.get("user", None)
        if user_data is None:
            raise exceptions.AuthenticationFailed("用户认证失败")
        user_obj = UserInfo.objects.filter(**user_data).first()
        return user_obj, None


class AdminAuthentication(authentication.BaseAuthentication):
    """用于验证用户是否是管理员"""

    def authenticate(self, request):
        user_data = request.session.get("user", None)
        assert user_data, exceptions.AuthenticationFailed("用户认证失败")
        user_obj = UserInfo.objects.get(**user_data)
        assert user_obj.user_type == 2, exceptions.AuthenticationFailed("用户没有权限")
        return user_obj, None
