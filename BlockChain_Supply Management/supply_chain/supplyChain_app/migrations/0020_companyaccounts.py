# Generated by Django 5.0.1 on 2024-02-29 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplyChain_app', '0019_sentmailmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=20)),
                ('available_amt', models.FloatField()),
            ],
        ),
    ]
