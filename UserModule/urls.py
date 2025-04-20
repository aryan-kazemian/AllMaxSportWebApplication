from django.urls import path
from .views import user_api

urlpatterns = [
    path('', user_api, name='user-api'),
]
