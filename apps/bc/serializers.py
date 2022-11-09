#序列化，没规则转为有规则
from rest_framework import serializers

from apps.goods.models import Goods
from apps.users.models import UserGender, Users


class CreateCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=200,allow_blank=False
    )
    password=serializers.CharField(
        max_length=200
    )
    first_name = serializers.CharField(
        max_length=200,
        error_messages={
            "blank":"first name is required",
            "max-length":"xxx"
        }
    )
    last_name = serializers.CharField(
        max_length=200
    )
    gender = serializers.ChoiceField(
        choices=[item.value for item in UserGender]
    )

    def validate(self,attrs):
        return attrs


class CreateOrderSerializer(serializers.Serializer):
    userid = serializers.CharField(
        max_length=200, allow_blank=False
    )
    adress = serializers.CharField(
        max_length=200,allow_blank=False
    )
    phone = serializers.CharField(
        max_length=20,allow_blank=False
    )
    goods = serializers.ListField(

    )
    def validate(self, attrs):
        user = attrs.get('userid')
        if not Users.objects.filter(id=user).first():
            raise serializers.ValidationError("User not exists")
        # 地址和订单id不能为空
        adress = attrs.get('adress')
        phone = attrs.get('phone')
        if adress=='' or phone=='':
            raise serializers.ValidationError("Please input adress and phone")
        #检验列表中的商品和数量
        for i in attrs.get('goods'):
            # 商品不能不存在
            good=i['goods-id']   #i是这样的 {'goods-id':1,'goods-num':2}
            _good = Goods.objects.filter(id=good).first()
            if not _good:
                raise serializers.ValidationError("Goods not exists")
            #库存不能不够
            num = i['goods-num']
            if _good.stock < num:
                raise serializers.ValidationError("Stock limited, you need to add less than {}".format(_good.stock))
        return attrs
