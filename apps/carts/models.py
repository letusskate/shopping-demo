from django.db import models

# Create your models here.
from apps.utils.base_model import BaseModel
from apps.users.models import Users
from apps.goods.models import Goods

#建立一个中间表，由于一个用户对应一个购物车，因此不需要建立购物车表，同时用户与商品构成m:n的关系，因此建立中间表存储添加购物车这个过程
class CartsGoods(BaseModel):
    user = models.ForeignKey(Users, related_name='user_cartsGoods', on_delete=models.CASCADE)
    good = models.ForeignKey(Goods, related_name='good_cartsGoods', on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    class Meta:
        db_table = 'cartsGoods'
        verbose_name = 'cartsGoods'
        verbose_name_plural = 'cartsGoods'
