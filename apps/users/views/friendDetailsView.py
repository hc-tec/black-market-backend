
from rest_framework.views import APIView\

from utils import statusCode, serializer
from utils.response import validData

from apps.users.models import UserInfo

class FriendDetails(APIView):

    @validData(statusCode.FriendDetails)
    def post(self, request, *args, **kwargs):
        friend_id = request.data.get("friend_id")
        friend = UserInfo.objects.filter(pk=friend_id).first()
        assert friend, "用户不存在"

        ser = serializer.ChatDetailsUserInfo(instance=friend)
        return {
            "data": ser.data
        }
