from rest_framework import serializers
from .models import (Cartitem, Color,
                     Order, OrderItems, 
                     Product, Category, Cart)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        
    def create(self, validated_data):
        category = super().create(validated_data)
        return CategorySerializer(
            category, context={"request": self.context.get("request")}
        ).data
        
    def update(self, instance, validated_data):
        category = super().update(instance, validated_data)
        return CategorySerializer(
            category, context={"request": self.context.get("request")}
        ).data

class ProductSerializerOut(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField('get_colors')
    category = serializers.CharField(source='category.title')
    
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'price',
            'description',
            'in_stock',
            'colors',
        ]
    
    def get_colors(self, obj : Product) -> list:
        return list(obj.colors.values_list('color', flat=True))
        
class ProductSerializerIn(serializers.ModelSerializer):
    colors = serializers.ListField()
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'in_stock', 'colors', 'category']
    
    def create(self, validated_data : dict):
        colors : list[str] = validated_data.pop('colors', None)
        colors_to_add = []
        if colors:
            for color in colors:
                color, created = Color.objects.get_or_create(color= color.lower())
                colors_to_add.append(color)
        try:
            product = Product.objects.create(**validated_data)
            
            for color in colors_to_add:
                product.in_colors.add(color)
            product.save()
            success = True
        except Exception as e:
            success = False
            # Handle or log the exception if necessary
            print(f"Error creating event: {e}")
        return ProductSerializerOut(
            product, context={"request": self.context.get("request")}
        ).data

    def update(self, instance, validated_data):
        colors : list[str] = validated_data.pop('colors', None)
        updated : Product = super().update(instance, validated_data)
        colors_to_add = []
        if colors:
            for color in colors:
                color, created = Color.objects.get_or_create(color= color.lower())
                colors_to_add.append(color)
        
        updated.in_colors.set(colors_to_add)
        updated.save()
        return ProductSerializerOut(
            updated, context={"request": self.context.get("request")}
        ).data

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitem
        fields = ['product', 'quantity']
        
    def create(self, validated_data):
        user = self.context['user_id']
        cart = Cart.objects.get_or_create(owner_id=user)
        cartitem = Cartitem.objects.create(
            cart=cart,
            **validated_data
        )
        return cartitem
        return super().create(validated_data)
    
    
class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id', 'cartitems']
        

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product', 'quantity',]
        
    def create(self, validated_data):
        user = self.context['user_id']
        order = Order.objects.get_or_create(owner_id=user)
        orderitems = OrderItems.objects.create(
            order=order,
            **validated_data
        )
        return orderitems
        return super().create(validated_data)
    
    
class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['order_id', 'order_items', 'is_verified']
        
        
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart = Cart.objects.filter(owner_id=user_id).first()
        cartitems = Cartitem.objects.filter(cart=cart).all()
        order = Order.objects.create(
            owner_id = user_id
        )
        for item in cartitems: 
            OrderItems.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity
            )
        return super().create(validated_data)
        