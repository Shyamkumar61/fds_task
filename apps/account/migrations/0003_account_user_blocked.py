# Generated by Django 4.0 on 2023-11-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
