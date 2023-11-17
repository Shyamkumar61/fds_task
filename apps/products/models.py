from django.db import models
from apps.account.models import Account
# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'
        permissions = [
            ("user_can_view", "User Can View"),
            ("user_can_add", "User Can Add"),
            ("user_can_edit", "User Can Edit")
        ]

    def __str__(self):
        return self.name


class Orders(models.Model):

    CASH_ON_DELIVERY = "cod"
    UPI = "upi"

    PENDING = 'pending'
    ASSIGNED = 'assigned'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    ORDER_CHOICES = (
        (PENDING, 'Pending'),
        (ASSIGNED, 'Assigned'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    )

    PAYMENT_CHOICES = (
        (CASH_ON_DELIVERY, 'Cash On Delivery'),
        (UPI, 'Upi')
    )

    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='customer_orders', limit_choices_to={
        'customer': True
    })
    product = models.ManyToManyField(Product)
    order_status = models.CharField(choices=ORDER_CHOICES, max_length=20, default=PENDING)
    order_address = models.TextField()
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=CASH_ON_DELIVERY)
    delivery_agent = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name='orders',
                                       limit_choices_to={'delivery_agent': True})
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'



class OrderItems(models.Model):

    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItem'


class OTPModel(models.Model):
    token = models.CharField(max_length=100)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
