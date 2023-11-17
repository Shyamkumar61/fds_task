from django.utils.crypto import get_random_string
from .models import OTPModel
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings


def generate_otp(user, order):
    otp = OTPModel(token=get_random_string(20), user_id=user, order=order)
    try:
        send_mail('Order Places', f"Please share the otp to Delivery Agent {otp.token}", settings.EMAIL_HOST_USER,
              user.email)
    except Exception as e:
        print(str(e))
    return otp
