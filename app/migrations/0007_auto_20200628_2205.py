# Generated by Django 2.1.9 on 2020-06-28 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_lecturesdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='User_Email',
            field=models.CharField(default='NA', max_length=70),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='User_FName',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='User_LName',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='User_Password',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='User_Phone',
            field=models.CharField(default='NA', max_length=15),
        ),
    ]
