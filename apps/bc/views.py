import json
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bc.serializers import CreateCustomerSerializer, CreateOrderSerializer

store_hash = 'lmmy6gqzw6'

class CreateBCCustomerView(APIView):
    authentication_classes = ()
    def post(self,request):
        url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/customers'
        headers = {
            "X-Auth-Token": "ok2x929wsy5zg20hsudb8yllmorg5yr",
            "Content-Type": "Application/json"
        }
        import json
        user_data = json.loads(request.body)
        serializer = CreateCustomerSerializer(data={
            "email": user_data.get("email"),
            "password": user_data.get("password"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "gender": user_data.get("gender"),
        })
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_user = requests.post(url, headers=headers, data=json.dumps([{
            "email": user_data['email'],
            "first_name": user_data['first_name'],
            "last_name": user_data['last_name']
        }]))
        return Response(new_user.json())

class CreateBCOrderView(APIView):
    def post(self,request):
        url = f'https://api.bigcommerce.com/stores/{store_hash}/v2/orders'
        headers = {
            "X-Auth-Token": "ok2x929wsy5zg20hsudb8yllmorg5yr",
            "Content-Type": "Application/json",
            "Accept": "application/json"
        }
        # # 先不用序列化器了
        # import json
        # data = json.loads(request.body)
        # serializer = CreateOrderSerializer(data={
        #     'userid': data.get('userid'),
        #     'adress': data.get('adress'),
        #     'phone': data.get('phone'),
        #     'goods': data.get('goods')
        # })
        # if not serializer.is_valid():
        #     return Response(serializer.errors)
        new_order = requests.post(url, headers=headers, data=request.body)
        return Response(new_order.json())


