
from django.db import transaction

from rest_framework.generics import ListAPIView

from utils import statusCode, serializer
from utils.response import validData

from apps.users.models.friendModel import (Friend, FRIEND_STATUS, UserInfo)

class FriendView(ListAPIView):

    serializer_class = serializer.FriendSerializer

    def get_serializer_context(self):
        return {
            "role": self.request._request.GET.get("role", "own")
        }

    def get_queryset(self):
        '''
        好友获取
        正在申请 & 申请被拒好友 | 正式好友
        '''
        params = self.request._request.GET

        role = params.get("role", "own")
        assert role in ("own", "friend"), "对象错误"

        friend_type = int(params.get("friend_type",
                    FRIEND_STATUS.APPLY_PASS))

        # 我 添加的好友以及我正在申请的好友以及被拒绝的好友
        if role == "own":
            # 获取正式好友列表
            friends = Friend.objects.filter(own_id=self.request.user)
            if friend_type == FRIEND_STATUS.APPLY_PASS:
                return friends.filter(
                    friend_status=FRIEND_STATUS.APPLY_PASS)
            # 获取 申请好友
            elif friend_type == FRIEND_STATUS.APPLYING:
                return friends.filter(
                        friend_status=FRIEND_STATUS.APPLYING)
            else:
                # 以及 被拒好友 列表
                return friends.filter(
                    friend_status=FRIEND_STATUS.APPLY_DENY)
        # 添加 我 为好友的
        elif role == "friend":
            friends = Friend.objects.filter(friend_id=self.request.user)
            return friends.filter(friend_status=FRIEND_STATUS.APPLYING)

    def get_friend(self, friend_id: int) -> any:

        assert friend_id, "用户 ID 不能为空"

        friend = UserInfo.objects.filter(pk=friend_id).first()
        assert friend, "此用户不存在"

        return friend

    @validData(statusCode.FriendApply)
    def post(self, request, *args, **kwargs):
        '''
        好友申请
        '''
        user = request.user
        friend_id = request.data.get("friend_id")
        action = request.data.get("action", "apply")
        friend = self.get_friend(friend_id)
        if action == "apply":
            apply_friend, is_new = Friend.objects.get_or_create(
                own_id=user, friend_id=friend)
            # 第一次添加好友
            if is_new: return
            # 被拒绝之后再次添加
            apply_friend.__dict__["friend_status"] = FRIEND_STATUS.APPLYING
            apply_friend.save()
        elif action == "revoke":
            # 撤销申请
            apply_friend = Friend.objects.filter(
                own_id=user, friend_id=friend).first()
            assert apply_friend.friend_status == FRIEND_STATUS.APPLYING, \
                    "好友状态不正确"
            apply_friend.delete()

    @validData(statusCode.FriendApplyPass)
    def put(self, request, *args, **kwargs):
        '''
        好友申请通过
        此时 user 是客体 Friend，而非主体 own
        '''

        user = request.user
        friend_id = request.data.get("friend_id")
        action = request.data.get("action", "accept")
        friend = self.get_friend(friend_id)

        apply_friend = Friend.objects.filter(
            own_id=friend, friend_id=user).first()

        assert apply_friend, "好友关系不存在"

        assert apply_friend.friend_status == \
               FRIEND_STATUS.APPLYING, \
            "好友状态不正确"

        if action == "accept":
            # 好友申请请求通过
            # 双方互相添加为好友
            with transaction.atomic():
                apply_friend.__dict__["friend_status"] = FRIEND_STATUS.APPLY_PASS
                apply_friend.save()
                apply_friend, _ = Friend.objects.get_or_create(
                    own_id=user, friend_id=friend)
                apply_friend.__dict__["friend_status"] = FRIEND_STATUS.APPLY_PASS
                apply_friend.save()
        elif action == "refuse":
            # 拒绝添加好友
            apply_friend.__dict__["friend_status"] = FRIEND_STATUS.APPLY_DENY
            apply_friend.save()

    @validData(statusCode.DeleteFriend)
    def delete(self, request, *args, **kwargs):
        '''
        删除好友
        只有已通过的申请的好友才能被删除
        '''
        user = request.user
        friend_id = request._request.GET.get("friend_id")

        friend = self.get_friend(friend_id)

        apply_friend = Friend.objects.filter(
            own_id=user, friend_id=friend).first()
        assert apply_friend, "好友关系不存在"

        assert apply_friend.friend_status == \
               FRIEND_STATUS.APPLY_PASS, \
                "好友状态不正确"

        # 好友删除
        # apply_friend.delete()
