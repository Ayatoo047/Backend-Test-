from django.db import models
import uuid
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    in_stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.IntegerField()

    def __str__(self):
        return str(self.name)

        