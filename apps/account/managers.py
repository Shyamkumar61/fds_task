from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


class AccountManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            return ValueError("Please Enter the Username")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('customer', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

    def create_delivery_agent(self, email, **extra_fields):
        extra_fields.setdefault('delivery_agent', True)
        password = get_random_string(12)
        print("Test")
        try:
            print("Test 1")
            send_mail(
                "Test",
                f"Username: {extra_fields['username']}, password: {password}",
                settings.EMAIL_HOST_USER,
                ["shyam6132@gamil.com"]
            )
        except Exception as e:
            print("test 2")
            print(str(e))
        return self._create_user(email, password, **extra_fields)


