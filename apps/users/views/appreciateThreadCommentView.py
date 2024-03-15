from django.db import transaction
from rest_framework.generics import ListAPIView

from apps.users.models import ThreadComment
# from apps.users.models.threadCommentModel import ThreadComment
from utils import statusCode
from utils.response import validData


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
            return {
                "num": comment_obj.comment_appreciate
            }
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
        return {
            "num": comment_obj.comment_appreciate
        }
