from django.urls import path
from .views import OrderAndDiscountCodeView

urlpatterns = [
    path('', OrderAndDiscountCodeView.as_view()),
]
