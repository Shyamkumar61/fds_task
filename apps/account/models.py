from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from .managers import AccountManager
# Create your models here.


def validate_name(value):
    if value and not value.isalpha():
        raise ValidationError("No Numbers are Allowed")
    return value


class Account(AbstractUser):

    email = models.EmailField(_("Email Field"), unique=True, max_length=30)
    username = models.CharField(_("username"), unique=True, max_length=20)
    first_name = models.CharField(_("first name"), max_length=20, validators=[validate_name])
    last_name = models.CharField(_("last_name"), max_length=20, validators=[validate_name])
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    delivery_agent = models.BooleanField(
        _("delivery agent"), default=False
    )
    customer = models.BooleanField(
        _("customer"), default=False
    )
    user_blocked = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = AccountManager()

    REQUIRED_FIELDS = ['username', 'phone_number']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name
