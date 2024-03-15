from rest_framework.views import APIView
from utils import statusCode
from utils.response import validData

from utils.serializer import UserInfoSerializer


class Exit(APIView):
    """
    退出登录接口
    """

    @validData(statusCode.Exit)
    def get(self, request, *args, **kwargs):
        ser = UserInfoSerializer(instance=request.user, many=False)
        request.session.flush()
        return ser.data
