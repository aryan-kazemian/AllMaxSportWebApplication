from django.contrib import admin
from .models import Order, DiscountCode

admin.site.register(Order)
admin.site.register(DiscountCode)