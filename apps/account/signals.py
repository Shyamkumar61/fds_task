from django.db.models.signals import Signal, post_save
from django.dispatch import receiver
from django.core.mail import send_mail, send_mass_mail
from apps.products.models import Orders
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string, get_template
from datetime import datetime
from django.utils.html import strip_tags


send_email = Signal()


@receiver(post_save, sender=Orders)
def send_email(sender, instance, created, **kwargs):
    if not created:
        if instance.order_status == 'cancelled':
            print('True')
            customer_message = (
                "Order Cancelled",
                f"Your Order of {', '.join(product.name for product in instance.product.all())} Cancelled By the Owner",
                settings.EMAIL_HOST_USER,
                [instance.customer.email]
            )

            agent_message = (
                "Order Cancelled",
                f"{instance.customer.first_name} Order of  {' '. join(product.name for product in instance.product.all())} Cancelled By the Owner",
                settings.EMAIL_HOST_USER,
                [instance.delivery_agent.email if instance.delivery_agent else None]
            )

            send_mass_mail([customer_message, agent_message])
