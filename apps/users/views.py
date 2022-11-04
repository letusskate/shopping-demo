import time

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import Users
import json

from apps.users.serializers import CreateUserSerializer


# Create your views here.

def get_userinfo(request):
    user = Users.objects.get(id=1)
    # print(user)
    result = render(request, 'userinfo.html', context={
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    })
    return result

class RegisterView(APIView):
    authentication_classes = ()
    def post(self,request):
        import json
        user_data = json.loads(request.body)
        serializer=CreateUserSerializer(data={
            "email":user_data.get("email"),
            "password": user_data.get("password"),
            "first_name":user_data.get("first_name"),
            "last_name":user_data.get("last_name"),
            "gender":user_data.get("gender"),
        })
        if not serializer.is_valid():
            return Response(serializer.errors)
        # create方法
        user = Users.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            gender=user_data['gender'],
            password=user_data['password']
        )

        cache.delete('user_data')#旁路模式，删除缓存

        # 创建用户
        return JsonResponse({'code': 200, 'message': 'success', "data": {
            "userId": user.id
        }})

class UserLoginView(APIView):
    authentication_classes = ()#不再token校验
    def post(self,request):
        data = json.loads(request.body)
        email = data.get('email')
        pswd = data.get('password')
        user = Users.objects.filter(email=email, password=pswd).first()
        if not user:
            return Response({
                'code':404,
                'message':"User data not exist"
            })
        # if user.password!=pswd:
        #     return Response({
        #         'code': 404,
        #         'message': "User password not correct"
        #     })
        payload={
            "email":email,
            # "exp":int(time.time())+30*60,
            "exp": int(time.time()) + 30 * 600000,
        }

        from django.conf import settings
        import jwt
        secret_key=settings.SECRET_KEY
        token = jwt.encode(payload,secret_key,algorithm='HS256').decode('utf-8')


        return Response({
            'code':200,
            'message':'success',
            'data':{
                'token':token
            }
        })

class ChangePasswordView(APIView):
    def post(self, request):
        pass

