# Generated by Django 2.1.12 on 2022-11-04 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default='123654', max_length=200),
        ),
    ]