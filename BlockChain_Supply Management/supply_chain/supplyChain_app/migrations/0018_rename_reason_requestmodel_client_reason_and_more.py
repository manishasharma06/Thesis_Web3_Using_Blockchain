# Generated by Django 5.0.1 on 2024-02-11 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplyChain_app', '0017_refundmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestmodel',
            old_name='reason',
            new_name='client_reason',
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='company_reason',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
