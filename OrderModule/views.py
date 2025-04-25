from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, DiscountCode
from ProductModule.models import Product
from UserModule.models import User
from .serializers import OrderSerializer, DiscountCodeSerializer
from django.shortcuts import get_object_or_404

class OrderAndDiscountCodeView(APIView):
    def get(self, request):
        discount_code_flag = request.query_params.get('discount_code')
        discount_code_id = request.query_params.get('discount_code_id')

        if discount_code_flag == 'true':
            if discount_code_id:
                code = get_object_or_404(DiscountCode, id=discount_code_id)
                serializer = DiscountCodeSerializer(code)
                return Response(serializer.data)
            else:
                codes = DiscountCode.objects.all()
                serializer = DiscountCodeSerializer(codes, many=True)
                return Response(serializer.data)

        # Filter Orders
        filters = {}
        if 'id' in request.query_params:
            filters['id'] = request.query_params.get('id')
        if 'order_id' in request.query_params:
            filters['order_id'] = request.query_params.get('order_id')
        if 'order_date' in request.query_params:
            filters['order_date'] = request.query_params.get('order_date')
        if 'order_status' in request.query_params:
            filters['order_status'] = request.query_params.get('order_status')
        if 'customer' in request.query_params:
            filters['customer_id'] = request.query_params.get('customer')

        orders = Order.objects.filter(**filters)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.query_params.get('discount_code') == 'true':
            serializer = DiscountCodeSerializer(data=request.data)
        else:
            serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data if hasattr(order, 'order_id') else serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')

        if discount_code_id:
            code = get_object_or_404(DiscountCode, id=discount_code_id)
            serializer = DiscountCodeSerializer(code, data=request.data, partial=True)
        elif order_id:
            order = get_object_or_404(Order, id=order_id)
            serializer = OrderSerializer(order, data=request.data, partial=True)
        else:
            return Response({"error": "No valid ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')

        if discount_code_id:
            code = get_object_or_404(DiscountCode, id=discount_code_id)
            code.delete()
            return Response({"message": "Discount code deleted"}, status=status.HTTP_200_OK)
        elif order_id:
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return Response({"message": "Order deleted"}, status=status.HTTP_200_OK)

        return Response({"error": "No valid ID provided"}, status=status.HTTP_400_BAD_REQUEST)
