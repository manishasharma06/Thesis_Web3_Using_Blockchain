# Generated by Django 4.1.5 on 2023-11-30 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplyChain_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mercedes_ordermodel',
            name='order_amt',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
