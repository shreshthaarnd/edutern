# Generated by Django 2.1.9 on 2020-06-28 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200627_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursedata',
            name='Course_Content',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='Join_Date',
            field=models.CharField(default='28/06/2020', max_length=50),
        ),
    ]
