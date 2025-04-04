# Generated by Django 5.0.1 on 2024-03-01 03:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplyChain_app', '0020_companyaccounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantModel',
            fields=[
                ('merchant', models.CharField(max_length=20)),
                ('ship_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('est_del', models.DateField()),
                ('type', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplyChain_app.ordermodel')),
            ],
        ),
    ]
