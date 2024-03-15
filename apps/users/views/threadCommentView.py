from django.db import transaction
from rest_framework.generics import ListAPIView

from apps.users.models import ThreadComment, UserInfo, Message, Thread
# from apps.users.models.threadCommentModel import ThreadComment
#
# from apps.users.models.threadModel import Thread
#
# from apps.users.models.userinfoModel import UserInfo
#
# from apps.users.models.messageModel import Message
from utils import statusCode
from utils.response import validData
from utils.serializer import ThreadCommentSerializer
from utils.pagination import ThreadCommentPagination


class ThreadCommentView(ListAPIView):
    serializer_class = ThreadCommentSerializer
    pagination_class = ThreadCommentPagination

    def get_serializer_context(self):
        return {
            "user": self.request.user
        }

    # 通过帖子id获得相应评论
    def get_queryset(self):
        thread_id = self.request.query_params["thread_id"]
        threadComment_obj = ThreadComment.objects\
            .filter(thread_info_id=thread_id, comment_parent_id=None)
        return threadComment_obj

    @validData(statusCode.ThreadCommentUpload)
    def post(self, request, *args, **kwargs):
        '''
        发布 [帖子评论]

        根据帖子 id + 用户的 id + 父评论 id 等
        将评论添加到相应的帖子评论区中
        '''
        try:
            user = request.user
            data = request.data
            user_obj = None
            thread_id = data.get("thread_id")
            comment_parent_id = data.get("comment_parent_id", None)
            comment_reply_id = data.get("comment_reply_id", None)
            comment_content = data.get("comment_content")
            thread_obj = Thread.objects.filter(pk=thread_id).first()
            assert thread_obj is not None, "帖子不存在"
            with transaction.atomic():
                user_obj = UserInfo.objects.filter(id=comment_reply_id).first()

                # 创建消息，回复了帖子或评论
                # 如果是在自己的帖子下评论则不创建消息
                if user != thread_obj.author_info:
                    if comment_reply_id is not None:
                        assert user_obj, "回复用户不存在"
                        Message.objects.create(author=user, message_content=user.user_name + "回复了你的评论",
                                               reply_user=user_obj, related_thread=thread_obj)
                    else:
                        Message.objects.create(author=user, message_content=user.user_name + "回复了你的帖子",
                                               related_thread=thread_obj, reply_user=thread_obj.author_info)
                thread_new = ThreadComment.objects.create(**{
                    "user_info": user,
                    "thread_info": thread_obj,
                    "comment_parent_id": comment_parent_id,
                    "comment_reply_id": user_obj,
                    "comment_content": comment_content,
                })
                return ThreadCommentSerializer(instance=thread_new, user=user).data
        except Exception as e:
            raise e

    @validData(statusCode.DeleteThreadComment)
    def delete(self, request, *args, **kwargs):
        """
        根据评论id删除评论
        """
        try:
            threadComment_id = request.data["threadComment_id"]
            comment_obj = ThreadComment.objects.filter(id=threadComment_id).first()
            assert comment_obj, "评论不存在"
            with transaction.atomic():
                comment_obj.delete()
            return
        except Exception as e:
            raise e


class AppreciateThreadComment(ListAPIView):

    def is_valid(self, request):
        user = request.user
        comment_id = request.data.get('comment_id')
        comment_obj = ThreadComment.objects.filter(pk=comment_id).first()

        assert comment_obj is not None, '评论不存在'
        return user, comment_obj

    def comment_appreciate_modify(self, comment_obj, num):
        appreciate_num = comment_obj.comment_appreciate
        comment_obj.__dict__['comment_appreciate'] = appreciate_num + num
        comment_obj.save()

    @validData(statusCode.AppreciateThreadComment)
    def put(self, request, *args, **kwargs):
        '''
        给 [帖子评论] 点赞
        根据点赞用户 + 帖子 id
        将用户加入到 [点赞用户] 中
        '''
        try:
            user, comment_obj = self.is_valid(request)
            # 将用户加入到 [点赞用户] 中
            # 添加数据库事务
            with transaction.atomic():
                comment_obj.appreciate_user.add(user)
                # 点赞数量 +1
                self.comment_appreciate_modify(comment_obj, 1)
        except Exception as e:
            raise Exception("点赞失败")

    @validData(statusCode.DeleteAppreciateThreadComment)
    def delete(self, request, *args, **kwargs):
        '''
        取消 [帖子评论] 点赞
        根据点赞用户 + 帖子 id
        # 将用户从 [点赞用户] 中移除
        '''
        user, comment_obj = self.is_valid(request)
        # 添加数据库事务
        with transaction.atomic():
            # 将用户从 [点赞用户] 中移除
            comment_obj.appreciate_user.remove(user)
            # 点赞数量 -1
            self.comment_appreciate_modify(comment_obj, -1)
