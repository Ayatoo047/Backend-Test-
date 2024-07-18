from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from customer.models import CustomerDetail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        
class CreateUserSerializerOut(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class LoginSerializerIn(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        user = authenticate(username=username, password=password)

        # if not user:
        #     raise InvalidRequestException(response)

        user_profile = CustomerDetail.objects.get_or_create(user=user)

        return user

        
    

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class CustomerSerializer(ModelSerializer):
    user = UserDetailSerializer
    class Meta:
        model = CustomerDetail
        fields = ['user', 'address', 'phone', 'state', 'country']
        
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        user = User.objects.get(id=user_id)
        return super().create(
            user=user,
            **validated_data
            )