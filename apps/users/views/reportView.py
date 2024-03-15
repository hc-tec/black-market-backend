from rest_framework.views import APIView
from django.db import transaction
from utils.response import validData
from utils import statusCode

from apps.users.models import GoodReport, ThreadReport, CommentReport


class GoodReportView(APIView):
    @validData(statusCode.GoodReport)
    def post(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            reason = request.data["reason"]
            other_reason = request.data.get("other_reason", None)
            good_id = request.data["good_id"]
            with transaction.atomic():
                # 写入举报信息
                GoodReport.objects.create(whistleblower=user_obj, reason=reason, other_reason=other_reason,
                                          related_good_id=good_id)
            return
        except Exception as e:
            raise e


class ThreadReportView(APIView):
    @validData(statusCode.ThreadReport)
    def post(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            reason = request.data["reason"]
            other_reason = request.data.get("other_reason", None)
            thread_id = request.data["thread_id"]
            with transaction.atomic():
                # 写入举报信息
                ThreadReport.objects.create(whistleblower=user_obj, reason=reason, other_reason=other_reason,
                                            related_thread_id=thread_id)
            return
        except Exception as e:
            raise e


class CommentReportView(APIView):
    @validData(statusCode.CommentReport)
    def post(self, request, *args, **kwargs):
        try:
            user_obj = request.user
            reason = request.data["reason"]
            other_reason = request.data.get("other_reason", None)
            comment_id = request.data["comment_id"]
            with transaction.atomic():
                # 写入举报信息
                CommentReport.objects.create(whistleblower=user_obj, reason=reason, other_reason=other_reason,
                                             related_comment_id=comment_id)
            return
        except Exception as e:
            raise e
