# Generated by Django 4.1.5 on 2023-12-04 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplyChain_app', '0007_alter_ordermodel_dt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='dt',
            field=models.DateTimeField(),
        ),
    ]
