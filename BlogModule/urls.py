from django.urls import path
from .views import blog_api

urlpatterns = [
    path('', blog_api),
]
