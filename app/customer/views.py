from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from app.customer.serializers import CustomerSerializer

# Create your views here.

class UpdateCustomerDetails():
    serializer_class = CustomerSerializer
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id}
    
    