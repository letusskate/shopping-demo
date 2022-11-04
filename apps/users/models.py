from django.db import models

# Create your models here.
from apps.utils.base_model import BaseModel
from enum import IntEnum


class UserGender(IntEnum):
    FEMALE = 0
    MALE = 1
    LADYBOY = 2

    @classmethod
    def choices(cls):
        return tuple(((item.value, item.name) for item in cls))


class Users(BaseModel):

    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    gender = models.SmallIntegerField(choices=UserGender.choices())

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'users'
        verbose_name = 'users'
        verbose_name_plural = 'users'
