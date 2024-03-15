
from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from utils.serializer import GoodSerializer

from ..search_indexes import GoodsIndex

class GoodsIndexSerializer(HaystackSerializer):

    object = serializers.SerializerMethodField()

    def get_object(self, row):
        return GoodSerializer(row, row.context["user"], read_only=True)

    class Meta:
        index_classes = [GoodsIndex] # 索引类的名称
        fields = ('text', 'object') # text 由索引类进行返回, object 由序列化类进行返回,第一个参数必须是text
