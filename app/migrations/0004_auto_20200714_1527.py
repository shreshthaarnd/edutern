# Generated by Django 2.1.9 on 2020-07-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_usercourses_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='Join_Date',
            field=models.CharField(default='14/07/2020', max_length=50),
        ),
        migrations.AlterModelTable(
            name='paymentdata',
            table='PaymentData',
        ),
    ]
