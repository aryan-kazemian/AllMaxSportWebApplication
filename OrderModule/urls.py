# urls.py
from django.urls import path
from .views import order_api
from . import views

urlpatterns = [
    path('', order_api, name='order_api'),
    path('discount_code/', views.discount_code_api, name='discount_code_api'),
]
