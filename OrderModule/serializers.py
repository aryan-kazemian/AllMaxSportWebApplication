from rest_framework import serializers
from .models import Order, DiscountCode
from UserModule.models import User
from ProductModule.models import Product


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    discount_code = serializers.PrimaryKeyRelatedField(queryset=DiscountCode.objects.all(), allow_null=True, required=False)
    items = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_id',
            'order_date',
            'order_status',
            'customer',
            'carrier',
            'cost',
            'estimated_delivery_date',
            'method',
            'code',
            'message',
            'authority',
            'fee_type',
            'fee',
            'discount_code',
            'items',
            'subtotal',
            'item_discount',
            'coupon_discount',
            'shipping',
            'tax',
            'total',
            'created_at',
            'updated_at',
            'shipped_at'
        ]
