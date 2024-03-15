from rest_framework.generics import ListAPIView
from django.db import transaction
from utils import statusCode
from utils.response import validData
from utils.serializer import (ThreadSerializer, GoodSerializer)
from utils import auth
# from apps.users.models.goodsModel import Goods
# from apps.users.models.threadModel import Thread
# from apps.users.models.messageModel import Message
from apps.users.models import (Goods, Thread, Message)


class GoodsAuditView(ListAPIView):
    # 只有管理员有权限访问这个接口
    authentication_classes = [auth.AdminAuthentication, ]
    serializer_class = GoodSerializer

    def get_queryset(self):
        return Goods.objects.exclude(flag=3001)

    @staticmethod
    def valid_audit_status(audit_status):
        for i in Goods.AUDIT_STATUS:
            if audit_status == str(i[0]):
                return True
        return False

    def send_audit_message(self, reply_user, audit_status: str):
        """根据审核状态码给用户发送相应消息"""
        if audit_status == "3000":
            Message.objects.create(author=self.request.user, reply_user=reply_user, message_content="您的商品正在等待管理员审核")
        elif audit_status == "3001":
            Message.objects.create(author=self.request.user, reply_user=reply_user, message_content="您的商品审核已通过")
        elif audit_status == "3002":
            Message.objects.create(author=self.request.user, reply_user=reply_user,
                                   message_content="您的商品审核未通过，请修改后重新提交")

    @validData(statusCode.GoodAudit)
    def put(self, request, *args, **kwargs):
        """通过获取商品id来更改商品审核状态"""
        good_id = request.data["good_id"]
        # 通过传递audit_status参数来更改审核状态
        audit_status = request.data["audit_status"]
        good_obj = Goods.objects.get(id=good_id)
        assert good_obj, "商品不存在"
        assert self.valid_audit_status(audit_status), "状态不存在"
        try:
            with transaction.atomic():
                # 更新审核状态
                good_obj.flag = audit_status
                good_obj.save()
                # 给用户发送相应消息
                self.send_audit_message(good_obj.seller, audit_status=audit_status)
        except Exception as e:
            raise e
        return


class ThreadAuditView(ListAPIView):
    # 只有管理员有权限访问这个接口
    authentication_classes = [auth.AdminAuthentication, ]
    serializer_class = ThreadSerializer

    @staticmethod
    def valid_audit_status(audit_status):
        for i in Thread.AUDIT_STATUS:
            if audit_status == str(i[0]):
                return True
        return False

    def send_audit_message(self, reply_user, audit_status: str):
        """根据审核状态码给用户发送相应消息"""
        if audit_status == "3000":
            Message.objects.create(author=self.request.user, reply_user=reply_user, message_content="您的帖子正在等待管理员审核")
        elif audit_status == "3001":
            Message.objects.create(author=self.request.user, reply_user=reply_user, message_content="您的帖子审核已通过")
        elif audit_status == "3002":
            Message.objects.create(author=self.request.user, reply_user=reply_user,
                                   message_content="您的帖子审核未通过，请修改后重新提交")

    def get_queryset(self):
        return Thread.objects.filter(flag=3000)

    @validData(statusCode.ThreadAudit)
    def put(self, request, *args, **kwargs):
        """通过获取帖子id来更改帖子审核状态"""
        thread_id = request.data["thread_id"]
        audit_status = request.data["audit_status"]
        thread_obj = Thread.objects.get(id=thread_id)
        assert thread_obj, "帖子不存在"
        assert self.valid_audit_status(audit_status), "状态不存在"
        try:
            with transaction.atomic():
                thread_obj.flag = audit_status
                thread_obj.save()
                # 审核状态改变给用户发送消息
                self.send_audit_message(audit_status=audit_status, reply_user=thread_obj.author_info)
        except Exception as e:
            raise e
        return
