from django.core.cache import cache
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.goods.models import Goods
from apps.orders.models import OrdersGoods, Orders
from apps.orders.serializers import MakeOrderSerializer, OrdersModelSerializer
from apps.users.models import Users


# Create your views here.
class MakeOrderView(APIView):
    def post(self,request):
        import json
        data=json.loads(request.body)
        serializer=MakeOrderSerializer(data={
            'userid':data.get('userid'),
            'goodsid':data.get('goodsid'),
            'ordersid':data.get('ordersid'),
            'goodsnum':data.get('goodsnum'),
            'adress':data.get('adress'),
            'phone':data.get('phone')
        })
        if not serializer.is_valid():
            return Response(serializer.errors)
        ordersid=data.get('ordersid')
        #如果没有订单，创建订单
        if ordersid=='':
            order = Orders.objects.create(
                user=Users.objects.filter(id=data['userid']).first(),
                adress=data['adress'],
                phone=data['phone'],
                value=0
            )
            ordersid=order.id
        # 订单中插入物品，注意减少物品库存，更新订单价格
        ordersGoods = OrdersGoods.objects.create(
            order=Orders.objects.filter(id=ordersid).first(),
            good=Goods.objects.filter(id=data['goodsid']).first(),
            num=data['goodsnum']
        )
        # 更新订单价格
        preprice=Orders.objects.filter(id=ordersid).first().value
        thisprice=data['goodsnum']*Goods.objects.filter(id=data['goodsid']).first().price
        Orders.objects.filter(id=ordersid).update(value=preprice+thisprice)
        # 更新物品库存
        prestock=Goods.objects.filter(id=data['goodsid']).first().stock
        Goods.objects.filter(id=data['goodsid']).update(stock=prestock-data['goodsnum'])
        return Response({'code': 200, 'message': 'success', "data": {
            "user-id": data['userid'],
            "orders-id": ordersid,
            "goods-id": data['goodsid'],
            "goods-num": data['goodsnum'],
            "pre order price":preprice,
            "this order price":thisprice,
            "order-total-price":preprice+thisprice,
            "adress":Orders.objects.filter(id=ordersid).first().adress,
            "phone":Orders.objects.filter(id=ordersid).first().phone
        }})

class GetOrdersView(APIView):
    def get(self, request):
        # 注意类型转换
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
        cache.delete('order_data')
        if cache.get('order_data'):
            orders = cache.get('order_data')
            order_data = OrdersModelSerializer(orders, many=True).data
            total_count = order_data.count()
        else:
            orders = Orders.objects.filter()
            total_count = orders.count()
            order_data = OrdersModelSerializer(orders, many=True).data  # 更简洁
            cache.set('order_data', order_data, timeout=600)
        _order_data = order_data[offset:offset + limit]


        return Response({
            "code": 200,
            'message': 'success',
            'data': {
                'list': _order_data,
                "pagination": {
                    "total_count": total_count,
                    'offset': offset,
                    "limit": limit,
                }
            }
        })