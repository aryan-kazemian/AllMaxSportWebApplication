# serializers.py
from rest_framework import serializers
from .models import Order
from ProductModule.models import Product
from UserModule.models import User
from .models import DiscountCode


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    items = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    discount_code = serializers.PrimaryKeyRelatedField(queryset=DiscountCode.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'order_date', 'order_status', 'customer', 'carrier', 'cost',
                  'estimated_delivery_date', 'method', 'code', 'message', 'authority', 'fee_type',
                  'fee', 'discount_code', 'items', 'subtotal', 'item_discount', 'coupon_discount',
                  'shipping', 'tax', 'total', 'created_at', 'updated_at', 'shipped_at']




class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'amount']