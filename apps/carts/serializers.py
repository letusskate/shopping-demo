#序列化，没规则转为有规则
from rest_framework import serializers


from apps.carts.models import CartsGoods
from apps.goods.models import Goods
from apps.users.models import Users


class AddCartsSerializer(serializers.Serializer):
    user = serializers.EmailField(
        max_length=200,allow_blank=False
    )
    good = serializers.CharField(
        max_length=200
    )
    num = serializers.IntegerField(

    )

    def validate(self,attrs):
        user = attrs.get('user')
        if not Users.objects.filter(id = user).first():
            raise serializers.ValidationError("User not exists")
        good = attrs.get('good')
        _good=Goods.objects.filter(id=good).first()
        if not _good:
            raise serializers.ValidationError("Goods not exists")
        num=attrs.get('num')
        if _good.stock < num:
            raise serializers.ValidationError("Stock limited, you need to add less than {}".format(_good.stock))
        return attrs



class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        # fields = ['id','first_name']
        # exclude = ['id']