from rest_framework.serializers import ModelSerializer
from app.customer.models import CustomerDetail
from django.contrib.auth.models import User


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