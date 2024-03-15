from rest_framework.views import APIView

from django.core.cache import cache

from utils import statusCode
from utils.encryption import creat_verification_code
from utils.response import validData

from utils.EmailSender import SendEmail


class GetCode(APIView):
    """
    获取验证码
    """

    @validData(statusCode.GetCode)
    def get(self, request, *args, **kwargs):
        user_obj = request.user
        # 生成验证码存储到Redis并设置有效期# 使用配置的redis数据库的别名，创建连接到redis的对象
        verification_code = creat_verification_code()
        cache.set(user_obj.pk, verification_code, 300)  # 该值的有效期为300s
        # 发送验证码
        qq = user_obj.qq
        email_sender = SendEmail(email_name="小黑市")
        email_sender.send(
            receiver_list=[user_obj.qq + "@qq.com", ],
            email_text="【小黑市】您的验证码为" + verification_code + "(5分钟有效，如非本人操作，请忽略。)",
            receiver_name=user_obj.user_name
        )
        # 记得退出
        email_sender.quit()
        return


class GetEmailCode(APIView):
    authentication_classes = []

    @validData(statusCode.GetCode)
    def post(self, request, *args, **kwargs):
        """
        邮箱认证接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        email = request.data["qq"] + "@qq.com"
        # 生成验证码存储到Redis并设置有效期# 使用配置的redis数据库的别名，创建连接到redis的对象
        verification_code = creat_verification_code()
        cache.set(email, verification_code, 300)  # 该值的有效期为300s
        # 发送验证码
        email_sender = SendEmail(email_name="华科二手市场")
        email_sender.send(
            receiver_list=[email, ],
            email_text="【小黑市】您的验证码为" + verification_code + "(5分钟有效，如非本人操作，请忽略。)",
            receiver_name=email
        )
        # 记得退出
        email_sender.quit()
        return
