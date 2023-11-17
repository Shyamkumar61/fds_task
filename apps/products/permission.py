from rest_framework.permissions import BasePermission, DjangoModelPermissions
from django.contrib.auth.models import Permission


class ProductPermission(BasePermission):
    """
    Custom permission to control access to Product objects.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return request.user.has_perm('products.user_can_view') or request.user.is_staff
        if request.method in ['GET', 'PUT', 'PATCH']:
            return request.user.has_perm('products.user_can_edit') or request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.has_perm('products.user_can_view')
        if request.method == "PUT":
            return request.user.is_staff
        return False


class AdminOrderPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class OrderPermission(BasePermission):
    """
    Custom permission to control access to Order objects.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            if request.user.customer or request.user.has_perm('products.view_order'):
                return True
        if request.method in ['GET', 'PUT', 'PATCH']:
            if request.user.customer or request.user.has_perm('products.edit_order'):
                return True
        return False


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.customer or request.user.is_staff
