# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Order, Product
from .serializers import OrderSerializer
from UserModule.models import User
from django.db.models import Q
from datetime import datetime


@csrf_exempt
def order_api(request):
    if request.method == 'GET':
        filters = Q()

        # Apply filters based on query params
        if 'id' in request.GET:
            filters &= Q(id=request.GET.get('id'))
        if 'order_id' in request.GET:
            filters &= Q(order_id=request.GET.get('order_id'))
        if 'customer' in request.GET:
            filters &= Q(customer_id=request.GET.get('customer'))
        if 'order_status' in request.GET:
            filters &= Q(order_status=request.GET.get('order_status'))
        if 'date_from' in request.GET:
            date_from = datetime.strptime(request.GET.get('date_from'), '%Y-%m-%d')
            filters &= Q(order_date__gte=date_from)
        if 'date_to' in request.GET:
            date_to = datetime.strptime(request.GET.get('date_to'), '%Y-%m-%d')
            filters &= Q(order_date__lte=date_to)
        if 'method' in request.GET:
            filters &= Q(method=request.GET.get('method'))
        if 'carrier' in request.GET:
            filters &= Q(carrier__icontains=request.GET.get('carrier'))

        orders = Order.objects.filter(filters)
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # Add order
        data = JSONParser().parse(request)
        customer_id = data.get('customer')
        if not customer_id:
            return JsonResponse({'error': 'Customer ID is required'}, status=400)

        customer = User.objects.get(id=customer_id)
        data['customer'] = customer  # Link customer

        # Handle order items (assuming IDs are passed in)
        item_ids = data.get('items')
        if not item_ids:
            return JsonResponse({'error': 'Items are required'}, status=400)

        items = Product.objects.filter(id__in=item_ids)
        if not items.exists():
            return JsonResponse({'error': 'Invalid product IDs'}, status=400)
        data['items'] = items  # Link items

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()  # Create order
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if 'id' in request.GET:
            try:
                order = Order.objects.get(id=request.GET.get('id'))
                order.delete()
                return JsonResponse({'message': 'Order deleted'})
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)

        return JsonResponse({'error': 'No valid delete identifier provided'}, status=400)

    elif request.method == 'PATCH':
        # Update order
        data = JSONParser().parse(request)
        if 'id' in request.GET:
            try:
                order = Order.objects.get(id=request.GET.get('id'))
                serializer = OrderSerializer(order, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, status=400)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)

        return JsonResponse({'error': 'No valid patch identifier provided'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


def discount_code_api(request):
    if request.method == 'GET':
        # Retrieve all discount codes or filter by ID
        if 'id' in request.GET:
            # Get a single discount code by ID
            discount_code = get_object_or_404(DiscountCode, id=request.GET.get('id'))
            serializer = DiscountCodeSerializer(discount_code)
            return JsonResponse(serializer.data)

        # If no 'id' filter, return a list of all discount codes
        discount_codes = DiscountCode.objects.all()
        serializer = DiscountCodeSerializer(discount_codes, many=True)
        return JsonResponse(serializer.data, safe=False)

    # POST - Create a new DiscountCode
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DiscountCodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # PATCH - Update an existing DiscountCode
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        if 'id' in request.GET:
            discount_code = get_object_or_404(DiscountCode, id=request.GET.get('id'))
            serializer = DiscountCodeSerializer(discount_code, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({'error': 'No valid patch identifier provided'}, status=400)

    # DELETE - Delete a DiscountCode
    elif request.method == 'DELETE':
        if 'id' in request.GET:
            try:
                discount_code = DiscountCode.objects.get(id=request.GET.get('id'))
                discount_code.delete()
                return JsonResponse({'message': 'Discount code deleted successfully'})
            except DiscountCode.DoesNotExist:
                return JsonResponse({'error': 'Discount code not found'}, status=404)
        return JsonResponse({'error': 'No valid delete identifier provided'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)