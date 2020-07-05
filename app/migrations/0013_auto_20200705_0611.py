# Generated by Django 2.1.9 on 2020-07-05 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_userreviews_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLectures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_ID', models.CharField(blank=True, max_length=20, null=True)),
                ('Course_ID', models.CharField(blank=True, max_length=20, null=True)),
                ('Lecture_ID', models.CharField(blank=True, max_length=20, null=True)),
                ('Lecture_Watched', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='userdata',
            name='Join_Date',
            field=models.CharField(default='05/07/2020', max_length=50),
        ),
    ]