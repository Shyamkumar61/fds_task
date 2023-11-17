from rest_framework.views import Response
from django.contrib.auth import get_user_model, authenticate
from .serializers import CreateCustomerAccount, CreateAgentAccount, LoginSerializer, \
            AccountSerializer, AgentSerializer, CustomerSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from apps.products.permission import CustomerPermission

User = get_user_model()


class RegisterCustomerView(generics.CreateAPIView):

    serializer_class = CreateCustomerAccount

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response({"success": "Account Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDeliveryAgent(generics.CreateAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CreateAgentAccount

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_agent(serializer.validated_data)
            return Response({"success": "Account Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # authentication_classes = [BasicAuthentication, SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Use get_or_create to get the existing token or create a new one
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountsView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = AccountSerializer


class ListAgentView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = User.objects.filter(delivery_agent=True)
        return queryset


class ListAgentDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = AgentSerializer

    def get_queryset(self):
        queryset = User.objects.filter(delivery_agent=True)
        return queryset


class ListCustomerView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.filter(customer=True)
    serializer_class = AccountSerializer


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.filter(customer=True)
    serializer_class = CustomerSerializer
    lookup_field = 'pk'

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'pk'

