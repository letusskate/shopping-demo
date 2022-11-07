from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
class AddCartsView(APIView):
    def post(self,request):
        import json
        data=json.loads(request.body)



class EditCartsView(APIView):
    def post(self,request):
        import json
        data=json.loads(request.body)
