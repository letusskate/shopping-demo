#序列化，没规则转为有规则
from rest_framework import serializers

from apps.goods.models import Goods


class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
        # fields = ['id','first_name']
        # exclude = ['id']