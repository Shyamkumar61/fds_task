# Generated by Django 4.0 on 2023-11-16 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('user_can_view', 'User Can View'), ('user_can_edit', 'User Can Edit')], 'verbose_name': 'Product', 'verbose_name_plural': 'Product'},
        ),
    ]