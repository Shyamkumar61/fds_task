from django.urls import path
from .views import ProductView, ProductDetailView, OrderView, OrderDetailUpdateView, AgentOrderView, \
    AgentOrderDetailsView, CustomerOrderView, CustomerOrderUpdateView, BulkUpload, task_status

urlpatterns = [
    path('product-list/', ProductView.as_view()),
    path('product-detail/<int:pk>/', ProductDetailView.as_view()),
    path('order-list/', OrderView.as_view()),
    path('order-detail/<int:pk>/', OrderDetailUpdateView.as_view()),
    path('agent-order/', AgentOrderView.as_view()),
    path('agent-order-detail/<int:pk>/', AgentOrderDetailsView.as_view()),
    path('user-orders/', CustomerOrderView.as_view()),
    path('user-order-detail/<int:pk>/', CustomerOrderUpdateView.as_view()),
    path('bulk-upload/', BulkUpload.as_view()),
    path('upload-status/', task_status),
]