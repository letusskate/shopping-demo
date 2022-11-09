from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.carts.models import CartsGoods
from apps.carts.serializers import AddCartsSerializer
from apps.goods.models import Goods
from apps.users.models import Users


# Create your views here.
class AddCartsView(APIView):
    def post(self,request):
        import json
        data=json.loads(request.body)
        serializer=AddCartsSerializer(data={
            'user':data.get('userid'),
            'good':data.get('goodsid'),
            'num':data.get('numbers'),
        })
        if not serializer.is_valid():
            return Response(serializer.errors)
        #如果购物车本身就有该商品，那么应该叠加数量；否则应该创建商品
        cartsGoods=CartsGoods.objects.filter(user=data['userid'], good=data['goodsid'])
        if not cartsGoods.first():
            carts=CartsGoods.objects.create(
                #外键新插入数据时，值应该等于主表中的对象，而不是主键
                user=Users.objects.filter(id=data['userid']).first(),
                good=Goods.objects.filter(id=data['goodsid']).first(),
                num=data['numbers']
            )
        else:
            cartsGoods.update(num=cartsGoods.first().num+data['numbers'])
            carts=cartsGoods.first() #显示的竟然是更新后的数据！
        cache.delete('carts_data')  # 旁路模式，删除缓存
        return JsonResponse({'code': 200, 'message': 'success', "data": {
            "user-id": carts.user.id,
            "user-name": carts.user.first_name+carts.user.last_name,
            "goods-id": carts.good.id,
            "goods-name":carts.good.name,
            "number" : carts.num
        }})

class EditCartsView(APIView):
    def post(self,request):
        import json
        data=json.loads(request.body)
        #可以和上面公用一个序列化器
        serializer = AddCartsSerializer(data={
            'user': data.get('userid'),
            'good': data.get('goodsid'),
            'num': data.get('numbers'),
        })
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = Users.objects.filter(pk=data['userid']).first()
        good = Goods.objects.filter(pk=data['goodsid']).first()
        #购物车物品和原先相同
        if data['numbers']==CartsGoods.objects.filter(user=user,good=good).first().num:
            return JsonResponse({
                'code': 404,
                'message': "your request has been satisfied"
            })
        #购物车删除物品
        elif data['numbers']==0:
            CartsGoods.objects.filter(user=user,good=good).delete()
        #购物车重新设置物品数量
        else:
            CartsGoods.objects.filter(user=user,good=good).update(num=data['numbers'])
        return JsonResponse({'code': 200, 'message': 'success', "data": {
            "user-id": user.id,
            "user-name": user.first_name+user.last_name,
            "goods-id": good.id,
            "goods-name": good.name,
            "new number": data['numbers']
        }})