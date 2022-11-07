from django.core.cache import cache
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.goods.models import Goods
from apps.goods.serializers import GoodsModelSerializer


# Create your views here.
class GoodsView(APIView):
    # authentication_classes = ()  # 不再token校验
    def get(self,request):
        id_query = request.GET.get('id')  # tom
        #注意类型转换
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
        if cache.get('goods_data'):
            goods_data = cache.get('goods_data')
            total_count = goods_data.count()
            return Response({
                "code": 200,
                'message': 'success',
                'data': {
                    'list': goods_data,
                    "pagination": {
                        "total_count": total_count,
                        'offset': offset,
                        "limit": limit,
                    }
                }
            })
        goods = Goods.objects.filter(
            # email__endswith=email_query
        )
        total_count = goods.count()
        _goods = goods[offset:offset + limit]

        goods_data = GoodsModelSerializer(_goods,many=True).data #更简洁

        cache.set('goods_data',goods_data,timeout=600)
        # _data=cache.get('user_data')
        # print(_data)  #测试缓存
        return Response({
            "code": 200,
            'message': 'success',
            'data': {
                'list': goods_data,
                "pagination": {
                    "total_count": total_count,
                    'offset': offset,
                    "limit": limit,
                }
            }
        })