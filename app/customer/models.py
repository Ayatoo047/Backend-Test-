from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerDetail(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=200)
    # last_name = models.CharField(max_length=200)
    # email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=11)
    # profile_image image = models.ImageField(null=True, blank=True)
    # dob =
    
    state = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=300, null=True)
    zipcode = models.CharField(max_length=10, null=True)