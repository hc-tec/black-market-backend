from rest_framework.views import APIView

from django.db import transaction
from utils import statusCode

from utils.response import validData

from apps.users.models import (Thread)
# from apps.users.models.threadModel import Thread
class AppreciateThread(APIView):

    def is_valid(self, request):
        user = request.user
        thread_id = request.data.get('thread_id')
        tread_obj = Thread.objects.filter(pk=thread_id).first()

        assert tread_obj is not None, '帖子不存在'
        return user, tread_obj

    def thread_appreciate_modify(self, thread_obj, num):
        appreciate_num = thread_obj.thread_appreciate
        thread_obj.__dict__['thread_appreciate'] = appreciate_num + num
        thread_obj.save()

    @validData(statusCode.AppreciateThread)
    def put(self, request, *args, **kwargs):
        '''
        给 [帖子评论] 点赞

        根据点赞用户 + 帖子 id
        将用户加入到 [点赞用户] 中
        '''
        try:
            user, thread_obj = self.is_valid(request)
            # 将用户加入到 [点赞用户] 中
            # 添加数据库事务
            with transaction.atomic():
                thread_obj.thread_appreciate_peoples.add(user)
                # 点赞数量 +1
                self.thread_appreciate_modify(thread_obj, 1)
            return {
                "num": thread_obj.thread_appreciate
            }
        except Exception as e:
            raise Exception("点赞失败")

    @validData(statusCode.DeleteAppreciateThread)
    def delete(self, request, *args, **kwargs):
        '''
        取消 [帖子评论] 点赞
        根据点赞用户 + 帖子 id
        # 将用户从 [点赞用户] 中移除
        '''
        user, thread_obj = self.is_valid(request)
        # 添加数据库事务
        with transaction.atomic():
            # 将用户从 [点赞用户] 中移除
            thread_obj.thread_appreciate_peoples.remove(user)
            # 点赞数量 -1
            self.thread_appreciate_modify(thread_obj, -1)
        return {
            "num": thread_obj.thread_appreciate
        }

class GetAppreciateThreadPeople(APIView):

    def is_valid(self, request):
        thread_id = request.query_params.get('thread_id')
        thread_obj = Thread.objects.filter(pk=thread_id).first()
        assert thread_obj is not None, '帖子不存在'
        return thread_obj

    @validData(statusCode.GetAppreciateThreadPeople)
    def get(self, request, *args, **kwargs):
        """
        详细的点赞用户获取
        """
        thread_obj = self.is_valid(request)
        appreciate_people = thread_obj.thread_appreciate_peoples.all()
        result = []
        for people in appreciate_people:
            result.append(people.user_name)
        return {"appreciate_people": result}
