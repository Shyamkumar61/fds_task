from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.


class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'username', 'first_name', 'last_name', 'delivery_agent', 'customer')
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('delivery_agent', 'customer')}),
    )

admin.site.register(Account, AccountAdmin)

