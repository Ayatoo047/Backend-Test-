from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from customer.serializers import CreateUserSerializer, CreateUserSerializerOut, CustomerSerializer, LoginSerializerIn
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# Create your views here.

class CustomersView(CreateModelMixin,
                    GenericViewSet):
    serializer_class = CustomerSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return super().get_serializer_class()
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id}
    

class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        print("Hello")
        serializer = LoginSerializerIn(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
                data={
                    "accessToken": f"{AccessToken.for_user(user)}",
                    "refreshToken": f"{RefreshToken.for_user(user)}",
                }
        )
    
    