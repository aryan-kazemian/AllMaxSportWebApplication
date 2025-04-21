# urls.py
from django.urls import path
from .views import product_category_api

urlpatterns = [
    path('', product_category_api, name='product-category-api'),
]
