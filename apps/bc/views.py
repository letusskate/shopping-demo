import json
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bc.serializers import CreateCustomerSerializer

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
        import json
        data = json.loads(request.body)
        serializer = CreateOrderSerializer(data={
            'userid': data.get('userid'),
            'adress': data.get('adress'),
            'phone': data.get('phone'),
            'goods': data.get('goods')
        })
        if not serializer.is_valid():
            return Response(serializer.errors)


def testCreateCustomer():
    url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/customers'
    headers = {
        "X-Auth-Token": "ok2x929wsy5zg20hsudb8yllmorg5yr",
        "Content-Type": "Application/json"
    }
    resp = requests.get(url,headers = headers)
    print(resp.status_code)

    new_user = requests.post(url,headers=headers,data=json.dumps([{
        "email":"string@ex.com",
        "first_name":"hhh",
        "last_name":"xxx"
    }]))
    # new_user = requests.post(url,headers=headers,data = json.dumps([{
    #     "email": "string3@example.com",
    #     "first_name": "string",
    #     "last_name": "string",
    #     "company": "string",
    #     "phone": "string",
    #     "notes": "string",
    #     "tax_exempt_category": "string",
    #     "customer_group_id": 0,
    #     "addresses": [
    #       {
    #         "address1": "Addr 1",
    #         "address2": "",
    #         "address_type": "residential",
    #         "city": "San Francisco",
    #         "company": "History",
    #         "country_code": "US",
    #         "first_name": "Ronald",
    #         "last_name": "Swimmer",
    #         "phone": "707070707",
    #         "postal_code": "33333",
    #         "state_or_province": "California",
    #         "form_fields": [
    #           {
    #             "name": "test",
    #             "value": "test"
    #           }
    #         ]
    #       }
    #     ],
    #     "authentication": {
    #       "force_password_reset": True,
    #       "new_password": "string123"
    #     },
    #     "accepts_product_review_abandoned_cart_emails": True,
    #     "store_credit_amounts": [
    #       {
    #         "amount": 43.15
    #       }
    #     ],
    #     "origin_channel_id": 1,
    #     "channel_ids": [
    #       1
    #     ],
    #     "form_fields": [
    #       {
    #         "name": "test",
    #         "value": "test"
    #       }
    #     ]
    # }]))
    print(new_user.status_code)

def testCreateOrder():
    
    resp = requests.get(url, headers=headers)
    print(resp.status_code)