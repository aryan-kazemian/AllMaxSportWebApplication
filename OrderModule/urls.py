from django.urls import path
from .views import OrderDiscountAPIView

urlpatterns = [
    path('', OrderDiscountAPIView.as_view()),
]
