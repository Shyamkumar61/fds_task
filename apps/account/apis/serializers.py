from django.db.models import Sum
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from apps.products.apis.serializers import OrderSerializer

User = get_user_model()


def validate_name(value):
    if value and not value.isalpha():
        raise ValidationError("No Numbers are Allowed")
    return value


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CreateCustomerAccount(serializers.Serializer):
    email = serializers.EmailField(max_length=30, required=True,
                                   style={
                                       'input_type': 'text',
                                       'placeholder': 'Email',
                                   })
    username = serializers.CharField(max_length=30, required=True, style={
                                       'input_type': 'text',
                                       'placeholder': 'username',
                                   })
    first_name = serializers.CharField(max_length=20, required=True, validators=[validate_name],
                                       style={
                                           'input_type': 'text',
                                           'placeholder': 'First Name',
                                       })
    last_name = serializers.CharField(max_length=20, required=True, validators=[validate_name],
                                      style={
                                          'input_type': 'text',
                                          'placeholder': 'Last Name',
                                      })
    phone_number = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={
            'input_type': 'password',
            'placeholder': 'Enter your password',
            'class': 'custom-password-field',
        }
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={
            'input_type': 'password',
            'placeholder': 'Enter your password',
            'class': 'custom-password-field',
        }
    )

    def validate(self, attrs):
        email = attrs.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists")

        for field_name, field_value in attrs.items():
            if field_value is None:
                raise ValidationError(f"{field_name} is required")

        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CreateAgentAccount(serializers.Serializer):

    email = serializers.EmailField(max_length=30, required=True,
                                   style={
                                       'input_type': 'text',
                                       'placeholder': 'Email',
                                   })
    username = serializers.CharField(max_length=30, required=True, style={
                                       'input_type': 'text',
                                       'placeholder': 'username',
                                   })
    first_name = serializers.CharField(max_length=20, required=True, validators=[validate_name],
                                       style={
                                           'input_type': 'text',
                                           'placeholder': 'First Name',
                                       })
    last_name = serializers.CharField(max_length=20, required=True, validators=[validate_name],
                                      style={
                                          'input_type': 'text',
                                          'placeholder': 'Last Name',
                                      })
    phone_number = serializers.CharField(max_length=20, required=True)

    def create_agent(self, validated_data):
        user = User.objects.create_delivery_agent(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )
        return user


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = []

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request'] if 'context' in kwargs and 'request' in kwargs['context'] else None
        if request and request.path == '/list-agent/':
            self.Meta.fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'delivery_agent',
        'user_blocked', 'user_permissions', 'groups']
        elif request and request.path == '/list-account/':
            self.Meta.fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'delivery_agent',
        'customer', 'user_blocked', 'user_permissions', 'groups']
        elif request and request.path == '/list-customer/':
            self.Meta.fields = ['email', 'username', 'first_name', 'last_name', 'phone_number',
                                'customer', 'user_blocked', 'user_permissions', 'groups']
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_permissions'] = [perm.name for perm in instance.user_permissions.all()]
        response['groups'] = [group.name for group in instance.groups.all()]
        return response


class AgentSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'delivery_agent',
        'user_blocked', 'user_permissions', 'groups', 'orders']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_permissions'] = [perm.name for perm in instance.user_permissions.all()]
        response['groups'] = [group.name for group in instance.groups.all()]
        return response


class CustomerSerializer(serializers.ModelSerializer):

    customer_orders = OrderSerializer(many=True, read_only=True)
    total_order_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'delivery_agent', 'customer',
        'user_blocked', 'user_permissions', 'groups', 'total_order_amount',  'customer_orders']



    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_permissions'] = [perm.name for perm in instance.user_permissions.all()]
        response['groups'] = [group.name for group in instance.groups.all()]
        return response

    def get_total_order_amount(self, instance):
        total_amount = instance.customer_orders.aggregate(total_amount=Sum('total_amount'))['total_amount']
        return total_amount if total_amount is not None else 0
