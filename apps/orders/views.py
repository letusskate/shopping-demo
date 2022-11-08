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
        # 订单中插入物品，如果已经有，那就增加数量，如果没有，那就创建
        ordergoods=OrdersGoods.objects.filter(order=ordersid,good=data['goodsid'])
        if not ordergoods.first():
            ordersGoods = OrdersGoods.objects.create(
                order=Orders.objects.filter(id=ordersid).first(),
                good=Goods.objects.filter(id=data['goodsid']).first(),
                num=data['goodsnum']
            )
        else:
            ordergoods.update(num=ordergoods.first().num+data['goodsnum'])
        # 更新订单价格
        preprice=Orders.objects.filter(id=ordersid).first().value
        thisprice=data['goodsnum']*Goods.objects.filter(id=data['goodsid']).first().price
        Orders.objects.filter(id=ordersid).update(value=preprice+thisprice)
        # 更新物品库存
        prestock=Goods.objects.filter(id=data['goodsid']).first().stock
        Goods.objects.filter(id=data['goodsid']).update(stock=prestock-data['goodsnum'])
        #删除缓存
        cache.delete('order_data')
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

        if cache.get('order_data'):
            order_data = cache.get('order_data')
            total_count = len(order_data)
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