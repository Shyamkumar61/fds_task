# Generated by Django 4.0 on 2023-11-16 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_account_user_blocked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('assigned', 'Assigned'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('order_address', models.TextField()),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('payment_method', models.CharField(choices=[('cod', 'Cash On Delivery'), ('upi', 'Upi')], default='cod', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(limit_choices_to={'customer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='customer_order', to='account.account')),
                ('delivery_agent', models.ForeignKey(blank=True, limit_choices_to={'delivery_agent': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('product', models.ManyToManyField(to='products.Product')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Order',
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.orders')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItem',
            },
        ),
    ]
