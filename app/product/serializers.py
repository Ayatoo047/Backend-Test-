from rest_framework import serializers
from .models import (Cartitems, Color,
                     Order, OrderItems, 
                     Product, Category, Cart)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
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
    category = serializers.CharField(source='category.name')
    
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
                product.colors.add(color)
            product.save()
            success = True
        except Exception as e:
            success = False
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
            updated.colors.set(colors_to_add)
        updated.save()
        return ProductSerializerOut(
            updated, context={"request": self.context.get("request")}
        ).data

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitems
        fields = ['id','product', 'quantity']
        
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart,_ = Cart.objects.get_or_create(owner_id=user_id)
        product = validated_data.get('product', None)
        quantity = validated_data.get('quantity', None)
        cartitem = Cartitems.objects.filter(cart=cart, product=product).first()
        if cartitem:
            cartitem.quantity += quantity
            cartitem.save()
            return cartitem
        cartitem = Cartitems.objects.create(
            cart=cart,
            **validated_data
        )
        return cartitem
        return super().create(validated_data)
    
    
    
    
class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id', 'owner', 'cartitems']
    
        

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product', 'quantity']
        
    def create(self, validated_data):
        user = self.context['user_id']
        order = Order.objects.get_or_create(owner_id=user)
        orderitems = OrderItems.objects.create(
            order=order,
            **validated_data
        )
        return orderitems
        return super().create(validated_data)
    
class CreateOrderSerializer(serializers.Serializer):
    user_id = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart = Cart.objects.filter(owner_id=user_id).first()
        cartitems = Cartitems.objects.filter(cart=cart).all()
        order = Order.objects.create(
            owner_id = user_id
        )
        for item in cartitems: 
            OrderItems.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity
            )
        return order
    

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','order_id', 'orderitems', 'is_verified']
        
        
        