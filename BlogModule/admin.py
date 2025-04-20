from django.contrib import admin
from .models import Blog, Tag, SEOStatus



admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(SEOStatus)