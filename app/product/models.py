from typing import Iterable
from django.db import models
import uuid
from django.contrib.auth.models import User

class Color(models.Model):
    color = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return str(self.color)
    
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.color = self.color.lower()
        return super().save()

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.name)
    
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.name = self.name.lower()
        return super().save()

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    in_stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.IntegerField()
    colors = models.ManyToManyField(Color, blank=True)
    amount_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner)

class Cartitem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.product)
        

class Order(models.Model):
    owner = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE) 
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    orderitems = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)