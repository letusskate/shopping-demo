import requests
import json
store_hash = 'lmmy6gqzw6'

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
    url=f'https://api.bigcommerce.com/stores/{store_hash}/v2/orders'
    headers = {
        "X-Auth-Token": "ok2x929wsy5zg20hsudb8yllmorg5yr",
        "Content-Type": "Application/json",
        "Accept": "application/json"
    }
    resp = requests.get(url, headers=headers)
    print(resp.status_code)

    # # 自己的数据就是不行
    # new_order=requests.post(url,headers=headers,data=json.dumps({
    #     "billing_address":{
    #         "street_1":"hhhhh",
    #         "zip":"11111111111"
    #     },
    #     "products":[
    #         {
    #             "name": "BigCommerce Coffee Mug",
    #
    #             "quantity":1
    #         }
    #     ]
    # }))
    new_order=requests.post(url,headers=headers,data=json.dumps({
      "billing_address": {
        "first_name": "Jane",
        "last_name": "Doe",
        "street_1": "123 Main Street",
        "city": "Austin",
        "state": "Texas",
        "zip": "78751",
        "country": "United States",
        "country_iso2": "US",
        "email": "janedoe@email.com"
      },
      "products": [
        {
          "name": "BigCommerce Coffee Mug",
          "quantity": 1,
          "price_inc_tax": 50,
          "price_ex_tax": 45
        }
      ]
    }))
    print(new_order.status_code)

if __name__=='__main__':
    testCreateCustomer()
    testCreateOrder()