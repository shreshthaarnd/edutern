# Generated by Django 2.1.9 on 2020-07-06 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20200706_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userreviews',
            name='Review_ID',
        ),
    ]