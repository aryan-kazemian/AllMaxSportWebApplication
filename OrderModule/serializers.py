from rest_framework import serializers
from .models import Order, DiscountCode

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    discount_code = serializers.PrimaryKeyRelatedField(read_only=True)
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'order_date', 'order_status', 'customer',
            'carrier', 'cost', 'estimated_delivery_date', 'method',
            'code', 'message', 'authority', 'fee_type', 'fee',
            'discount_code', 'items', 'subtotal', 'item_discount',
            'coupon_discount', 'shipping', 'tax', 'total',
            'created_at', 'updated_at', 'shipped_at'
        ]

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'
