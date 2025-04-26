from rest_framework import serializers
from .models import Order, OrderItem, DiscountCode
from ProductModule.models import Product

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'amount']

class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=12, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'quantity', 'price']

class CreateOrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'order_date', 'customer', 'carrier', 'order_status',
            'method', 'code', 'estimated_delivery_date', 'items',
            'subtotal', 'shipping', 'tax', 'total'
        ]

class CreateOrderSerializer(serializers.ModelSerializer):
    items = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'order_date', 'order_status', 'customer', 'customer_name',
            'carrier', 'cost', 'estimated_delivery_date', 'method', 'code', 'message',
            'authority', 'fee_type', 'fee', 'items',
            'subtotal', 'item_discount', 'coupon_discount', 'shipping', 'tax', 'total',
            'created_at', 'updated_at', 'shipped_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.order_items.all().delete()
            for item in items_data:
                product = Product.objects.get(id=item['id'])
                OrderItem.objects.create(order=instance, product=product, quantity=item['quantity'])
        return instance
