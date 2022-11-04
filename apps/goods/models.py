from django.db import models

# Create your models here.
from apps.utils.base_model import BaseModel
from enum import IntEnum


class GoodsKind(IntEnum):
    foods = 0
    cloths = 1
    using = 2

    @classmethod
    def choices(cls):
        return tuple(((item.value, item.name) for item in cls))

class Goods(BaseModel):
    name=models.CharField(max_length=200)
    price=models.DecimalField(decimal_places=2,max_digits=15)
    kind=models.SmallIntegerField(choices=GoodsKind.choices())
    stock=models.IntegerField(default=0)
    # pic=models.ImageField(null=True)#要安装pillow，很麻烦不装了
    introduce=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods'
        verbose_name = 'goods'
        verbose_name_plural = 'goods'