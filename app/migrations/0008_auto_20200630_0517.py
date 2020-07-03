# Generated by Django 2.1.9 on 2020-06-30 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200628_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Course_ID', models.CharField(max_length=20)),
                ('Course_Name', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='userdata',
            name='Join_Date',
            field=models.CharField(default='30/06/2020', max_length=50),
        ),
        migrations.AddField(
            model_name='usercourses',
            name='UserID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.UserData'),
        ),
    ]