# Generated by Django 2.1.9 on 2020-07-13 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentData',
            fields=[
                ('Pay_ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('CURRENCY', models.CharField(blank=True, default='None', max_length=100)),
                ('GATEWAYNAME', models.CharField(blank=True, default='None', max_length=100)),
                ('RESPMSG', models.CharField(blank=True, default='None', max_length=1000)),
                ('BANKNAME', models.CharField(blank=True, default='None', max_length=100)),
                ('PAYMENTMODE', models.CharField(blank=True, default='None', max_length=100)),
                ('RESPCODE', models.CharField(blank=True, default='None', max_length=100)),
                ('TXNID', models.CharField(blank=True, default='None', max_length=100)),
                ('TXNAMOUNT', models.CharField(blank=True, default='None', max_length=100)),
                ('STATUS', models.CharField(blank=True, default='None', max_length=100)),
                ('BANKTXNID', models.CharField(blank=True, default='None', max_length=100)),
                ('TXNDATE', models.CharField(blank=True, default='None', max_length=100)),
                ('CHECKSUMHASH', models.CharField(blank=True, default='None', max_length=100)),
            ],
            options={
                'db_table': 'PaymentData2',
            },
        ),
        migrations.AddField(
            model_name='usercourses',
            name='Pay_ID',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
