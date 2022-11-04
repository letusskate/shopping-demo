from django.db import models

# Create your models here.
from apps.utils.base_model import BaseModel
from apps.users.models import Users
from apps.goods.models import Goods

#用户与订单构成1：n关系，因此在订单中添加用户的外键
class Orders(BaseModel):
    user = models.ForeignKey(Users, related_name='user_orders', on_delete=models.CASCADE)
    class Meta:
        db_table = 'orders'
        verbose_name = 'orders'
        verbose_name_plural = 'orders'

#订单与商品构成m：n关系，因此创建中间表储存下单的过程
class OrdersGoods(BaseModel):
    order = models.ForeignKey(Orders, related_name='user_ordersGoods', on_delete=models.CASCADE)
    good = models.ForeignKey(Goods, related_name='good_ordersGoods', on_delete=models.CASCADE)
    num = models.IntegerField()
    class Meta:
        db_table = 'ordersGoods'
        verbose_name = 'ordersGoods'
        verbose_name_plural = 'ordersGoods'
