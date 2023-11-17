from django.urls import path
from .views import RegisterCustomerView, RegisterDeliveryAgent, LoginView, AccountsView, AccountDetailView, ListAgentView, \
                ListAgentDetailView, ListCustomerView, CustomerDetailView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register-user/', RegisterCustomerView.as_view()),
    path('register-agent/', RegisterDeliveryAgent.as_view()),
    path('list-account/', AccountsView.as_view()),
    path('list-agent/', ListAgentView.as_view()),
    path('list-customer/', ListCustomerView.as_view()),
    path('agent-detail/<int:pk>/', ListAgentDetailView.as_view()),
    path('customer-detail/<int:pk>/', CustomerDetailView.as_view()),
    path('account/<int:pk>/', AccountDetailView.as_view())
]
