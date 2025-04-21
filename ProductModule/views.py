# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Q

@csrf_exempt
def product_category_api(request):
    if request.method == 'GET':
        if request.GET.get('show_categories') == 'true':
            categories = Category.objects.all().values('id', 'name')
            return JsonResponse(list(categories), safe=False)

        filters = Q()
        if 'id' in request.GET:
            filters &= Q(id=request.GET.get('id'))
        if 'name' in request.GET:
            filters &= Q(name__icontains=request.GET.get('name'))
        if 'max_price' in request.GET:
            filters &= Q(price__lte=request.GET.get('max_price'))
        if 'min_price' in request.GET:
            filters &= Q(price__gte=request.GET.get('min_price'))
        if 'category' in request.GET:
            filters &= Q(category__name__icontains=request.GET.get('category'))
        if 'brand' in request.GET:
            filters &= Q(brand__icontains=request.GET.get('brand'))
        if 'status' in request.GET:
            filters &= Q(status=request.GET.get('status'))
        if 'sales' in request.GET:
            filters &= Q(sales=request.GET.get('sales'))

        products = Product.objects.filter(filters)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        if request.GET.get('add_category') == 'true':
            data = JSONParser().parse(request)
            name = data.get('name')
            if name:
                category, created = Category.objects.get_or_create(name=name)
                return JsonResponse({'id': category.id, 'name': category.name, 'created': created})
            return JsonResponse({'error': 'Category name required'}, status=400)

        data = JSONParser().parse(request)
        category_name = data.get('category')
        if not category_name:
            return JsonResponse({'error': 'Category is required'}, status=400)

        category, _ = Category.objects.get_or_create(name=category_name)
        data['category'] = category.name

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if 'id' in request.GET:
            try:
                product = Product.objects.get(id=request.GET.get('id'))
                product.delete()
                return JsonResponse({'message': 'Product deleted'})
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)

        if 'category_id' in request.GET:
            try:
                category = Category.objects.get(id=request.GET.get('category_id'))
                category.delete()
                return JsonResponse({'message': 'Category deleted'})
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)

        return JsonResponse({'error': 'No valid delete identifier provided'}, status=400)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)

        if 'id' in request.GET:
            try:
                product = Product.objects.get(id=request.GET.get('id'))
                serializer = ProductSerializer(product, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, status=400)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)

        if 'category_id' in request.GET:
            try:
                if 'id' in data:
                    return JsonResponse({'error': 'Cannot change category ID'}, status=400)
                category = Category.objects.get(id=request.GET.get('category_id'))
                serializer = CategorySerializer(category, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, status=400)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)

    return JsonResponse({'message': 'Method not allowed'}, status=405)
