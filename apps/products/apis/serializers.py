from django.db.models import Sum
from rest_framework import serializers
from apps.products.models import Product, Orders, OrderItems, OTPModel
from datetime import timedelta
from django.utils.crypto import get_random_string
from apps.products.utils import generate_otp



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = '__all__'

    def create(self, validated_data):
        product = validated_data.get('product')
        order = super().create(validated_data)
        total_amount = 0
        for product_id in product:
            OrderItems.objects.create(order=order, product_id=product_id, quantity=1)
            total_amount = total_amount + (product_id.price * 1)
        order.total_amount = total_amount
        order.save()
        return order

    def to_representation(self, instance):
        resoponse = super().to_representation(instance)
        resoponse['customer'] = instance.customer.first_name
        resoponse['delivery_agent'] = instance.delivery_agent.first_name if instance.delivery_agent else None
        resoponse['product'] = [{"name": item.name, "price": item.price} for item in instance.product.all()]
        return resoponse


class CustomerOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('order_address', 'order_status', 'product', 'payment_method')
        read_only_fields = ('delivery_agent', 'total_amount')

    def create(self, validated_data):
        product = validated_data.get('product')
        validated_data['customer'] = self.context.get('customer')
        order = super().create(validated_data)
        total_amount = 0
        for product_id in product:
            OrderItems.objects.create(order=order, product_id=product_id, quantity=1)
            total_amount = total_amount + (product_id.price * 1)
        order.total_amount = total_amount
        order.save()
        get_otp = generate_otp(user=self.context.get('customer'), order=order)
        return order

    def to_representation(self, instance):
        resoponse = super().to_representation(instance)
        resoponse['customer'] = instance.customer.first_name
        resoponse['delivery_agent'] = instance.delivery_agent.first_name if instance.delivery_agent else None
        resoponse['product'] = [{"name": item.name, "price": item.price} for item in instance.product.all()]
        return resoponse


class AgentOrderSerializer(serializers.ModelSerializer):

    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    ORDER_CHOICES = (
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    )

    otp = serializers.CharField()
    order_status = serializers.ChoiceField(choices=ORDER_CHOICES)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('order_status','total_amount')

    def to_representation(self, instance):
        resoponse = super().to_representation(instance)
        resoponse['customer'] = instance.customer.first_name
        resoponse['delivery_agent'] = instance.delivery_agent.first_name
        resoponse['product'] = [{"name": item.name, "price": item.price} for item in instance.product.all()]
        return resoponse

    def get_total_amount(self, instance):
        total_amount = instance.product.all().aggregate(total_amount=Sum('price'))['total_amount']
        return total_amount


class CustomerOrderUpdateSerializer(serializers.ModelSerializer):

    CANCELLED = 'cancelled'

    ORDER_CHOICES = (
        (CANCELLED, 'Cancelled')
    )

    order_status = serializers.ChoiceField(choices=ORDER_CHOICES)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('order_status', 'total_amount')

    def to_representation(self, instance):
        resoponse = super().to_representation(instance)
        resoponse['customer'] = instance.customer.first_name
        resoponse['delivery_agent'] = instance.delivery_agent.first_name if instance.delivery_agent else None
        resoponse['product'] = [{"name": item.name, "price": item.price} for item in instance.product.all()]
        return resoponse

    def get_total_amount(self, instance):
        total_amount = instance.product.all().aggregate(total_amount=Sum('price'))['total_amount']
        return total_amount


class VerifyOtpModule(serializers.Serializer):

    token = serializers.CharField(max_length=100)


class BulkUploadExcel(serializers.Serializer):

    excel_file = serializers.FileField()

