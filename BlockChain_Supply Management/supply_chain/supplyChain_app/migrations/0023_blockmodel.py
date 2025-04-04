# Generated by Django 5.0.1 on 2024-03-01 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplyChain_app', '0022_merchantmodel_remarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockModel',
            fields=[
                ('block_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('sender', models.CharField(max_length=20)),
                ('receiver', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplyChain_app.ordermodel')),
            ],
        ),
    ]
