from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, DiscountCode, Product
from .serializers import OrderSerializer, DiscountCodeSerializer
from datetime import datetime


class OrderAPI(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("query")
        discount_code_id = request.query_params.get("discount_code_id")

        filters = {}
        for field in ['id', 'order_id', 'order_date', 'order_status', 'customer', 'method', 'code']:
            val = request.query_params.get(field)
            if val:
                if field == 'order_date':
                    try:
                        filters['order_date'] = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        return Response({"error": "Invalid date format. Use ISO format."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    filters[field] = val

        if query == "discount_code":
            if discount_code_id:
                discount_code = get_object_or_404(DiscountCode, id=discount_code_id)
                serializer = DiscountCodeSerializer(discount_code)
                return Response(serializer.data)
            discount_codes = DiscountCode.objects.all()
            serializer = DiscountCodeSerializer(discount_codes, many=True)
            return Response(serializer.data)

        orders = Order.objects.filter(**filters) if filters else Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.query_params.get("query") == "discount_code":
            serializer = DiscountCodeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle POST for Order
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure we properly handle 'items' as ManyToMany relation
            if 'items' in request.data:
                items_ids = request.data['items']
                items = Product.objects.filter(id__in=items_ids)
                serializer.validated_data['items'] = items

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        order_id = request.query_params.get("id")
        discount_code_id = request.query_params.get("discount_code_id")

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if discount_code_id:
            discount_code = get_object_or_404(DiscountCode, id=discount_code_id)
            serializer = DiscountCodeSerializer(discount_code, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Missing id or discount_code_id"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        order_id = request.query_params.get("id")
        discount_code_id = request.query_params.get("discount_code_id")

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return Response({"message": "Order deleted"}, status=status.HTTP_200_OK)

        if discount_code_id:
            discount_code = get_object_or_404(DiscountCode, id=discount_code_id)
            discount_code.delete()
            return Response({"message": "Discount code deleted"}, status=status.HTTP_200_OK)

        return Response({"error": "Missing id or discount_code_id"}, status=status.HTTP_400_BAD_REQUEST)
