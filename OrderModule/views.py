from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, DiscountCode
from .serializers import OrderSerializer, CreateOrderSerializer, DiscountCodeSerializer
from django.shortcuts import get_object_or_404

class OrderDiscountAPIView(APIView):
    def get(self, request):
        discount_code = request.query_params.get('discount_code')
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')

        if discount_code == 'true':
            discounts = DiscountCode.objects.all()
            serializer = DiscountCodeSerializer(discounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if discount_code_id:
            discount = get_object_or_404(DiscountCode, id=discount_code_id)
            serializer = DiscountCodeSerializer(discount)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        discount_code = request.query_params.get('discount_code')

        if discount_code == 'true':
            serializer = DiscountCodeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')

        if discount_code_id:
            discount = get_object_or_404(DiscountCode, id=discount_code_id)
            serializer = DiscountCodeSerializer(discount, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            serializer = CreateOrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Missing id or discount_code_id'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')

        if discount_code_id:
            discount = get_object_or_404(DiscountCode, id=discount_code_id)
            discount.delete()
            return Response({'detail': 'Discount code deleted.'}, status=status.HTTP_204_NO_CONTENT)

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return Response({'detail': 'Order deleted.'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'detail': 'Missing id or discount_code_id'}, status=status.HTTP_400_BAD_REQUEST)
