from django.shortcuts import render
from apps.users.models import Users
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
