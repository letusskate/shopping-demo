from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.users.models import Users
from apps.carts.models import CartsGoods
from apps.goods.models import Goods
from apps.orders.models import Orders,OrdersGoods
from django.contrib.auth.models import User, Group


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'gender']
admin.site.register(CartsGoods)
admin.site.register(Goods)
admin.site.register(Orders)
admin.site.register(OrdersGoods)
