# Generated by Django 2.1.9 on 2020-07-13 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200713_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourses',
            name='Coupon',
            field=models.CharField(default='Not Applied', max_length=20),
        ),
    ]
