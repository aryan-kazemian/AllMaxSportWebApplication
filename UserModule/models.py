from django.contrib.auth.models import AbstractUser
from django.db import models


USER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

class User(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    phone = models.CharField(max_length=11)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    address_name = models.CharField(max_length=120, null=True, blank=True)
    address_phone = models.CharField(max_length=11, null=True, blank=True)
    province = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    delivery_notes = models.TextField(null=True, blank=True)
    total_orders = models.IntegerField(null=True, blank=True)
    total_spent = models.IntegerField(null=True, blank=True)
    average_order_value = models.FloatField(null=True, blank=True)
    first_purchase_date = models.DateField(null=True, blank=True)
    last_purchase_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    password_last_changed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
