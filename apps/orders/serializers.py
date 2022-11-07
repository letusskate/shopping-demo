#序列化，没规则转为有规则
from rest_framework import serializers

from apps.goods.models import Goods
from apps.orders.models import Orders
from apps.users.models import Users


class MakeOrderSerializer(serializers.Serializer):
    userid = serializers.CharField(
        max_length=200,allow_blank=False
    )
    #如果新建一个订单，可以为空
    ordersid = serializers.CharField(
        max_length=200,allow_blank=True
    )
    goodsid = serializers.CharField(
        max_length=200,allow_blank=False
    )
    goodsnum = serializers.IntegerField(
    )
    #如果订单本身就存在，可以为空
    adress = serializers.CharField(
        max_length=200,allow_blank=True
    )
    phone = serializers.CharField(
        max_length=20,allow_blank=True
    )
    def validate(self, attrs):
        user = attrs.get('userid')
        if not Users.objects.filter(id=user).first():
            raise serializers.ValidationError("User not exists")
        order=attrs.get('ordersid')
        #地址和订单id不能同时为空
        error1=True
        #如果订单不为空，订单不能不存在
        if order!='':
            error1=False
            if not Orders.objects.filter(id=order).first():
                raise serializers.ValidationError("Order not exists")
        #商品不能不存在
        good = attrs.get('goodsid')
        _good = Goods.objects.filter(id=good).first()
        if not _good:
            raise serializers.ValidationError("Goods not exists")
        #库存不能不够
        num = attrs.get('goodsnum')
        if _good.stock < num:
            raise serializers.ValidationError("Stock limited, you need to add less than {}".format(_good.stock))
        # 地址和订单id不能同时为空
        adress = attrs.get('adress')
        phone = attrs.get('phone')
        error2=True
        if adress!='' and phone!='':
            error2=False
        if error1 and error2:
            raise serializers.ValidationError("Please input order id or order adress and phone number")
        return attrs



class OrdersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        # fields = ['id','first_name']
        # exclude = ['id']