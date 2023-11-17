from django.http import JsonResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.views import Response
from rest_framework import generics
from apps.products.models import Product, Orders, OTPModel
from .serializers import ProductSerializer, OrderSerializer, AgentOrderSerializer, CustomerOrderSerializer, \
    CustomerOrderUpdateSerializer, BulkUploadExcel, VerifyOtpModule
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from apps.products.permission import ProductPermission, OrderPermission, DjangoModelPermissions, AdminOrderPermission, \
    CustomerPermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from openpyxl import load_workbook
from apps.products.tasks import process_bulk_upload
from celery.result import AsyncResult
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.shortcuts import get_object_or_404


class ProductView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [ProductPermission]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [ProductPermission]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class OrderView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Orders.objects.all()
        else:
            queryset = Orders.objects.filter(customer=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class OrderDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOrderPermission]

    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'


class AgentOrderView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]

    queryset = Orders.objects.all()
    serializer_class = ''

    def get_queryset(self):
        queryset = Orders.objects.filter(delivery_agent=self.request.user)
        return queryset


class AgentOrderDetailsView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    queryset = Orders.objects.all()
    serializer_class = AgentOrderSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Orders.objects.filter(delivery_agent=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        allowed_status = ['delivered', 'cancelled']
        otp = request.data.get('otp', '')
        order_status = request.data.get('order_status', '').lower()
        if order_status not in allowed_status:
            return Response({"error": "You are not Allowed"}, status=status.HTTP_403_FORBIDDEN)
        if order_status == 'delivered':
            order = self.get_object()
            otp_instance = get_object_or_404(OTPModel, order_id=order.id)
            if otp != otp_instance.token:
                return Response({"error": "Incorrect OTP"}, status=status.HTTP_403_FORBIDDEN)
            otp_instance.status = False
            otp_instance.save()
        return super().update(request, *args, **kwargs)


class CustomerOrderView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [OrderPermission]

    queryset = Orders.objects.all()
    serializer_class = CustomerOrderSerializer

    def get_queryset(self):
        queryset = Orders.objects.filter(customer=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'customer': self.request.user}


class CustomerOrderUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CustomerPermission]

    queryset = Orders.objects.all()
    serializer_class = CustomerOrderUpdateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Orders.objects.filter(customer=4)
        return queryset

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        created_at = order.created_at
        current_time = timezone.now()
        allowed_status = ['cancelled']
        order_status = request.data.get('order_status', '').lower()
        if order_status not in allowed_status:
            return Response({"error": "You are not Allowed"}, status=status.HTTP_403_FORBIDDEN)
        time_difference = (current_time - created_at).total_seconds() / 60
        if time_difference > 30:
            return Response({"error": "Update not allowed after 30 minutes"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class BulkUpload(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = BulkUploadExcel

    def post(self, request, *args, **kwargs):
        serializer = BulkUploadExcel(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['excel_file']
            task = process_bulk_upload.delay(excel_file.name, excel_file.read())
            return Response({'task_id': task.id})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def task_status(request, task_id):
    task = AsyncResult(task_id)
    result = {
        'current_state': task.state
    }
    if task.state == 'PROGRESS':
        result['progress'] = task.info
    return JsonResponse(result)
