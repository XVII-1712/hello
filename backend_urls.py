# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from core.views import index  # Import the view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('', index),  # Add this line
]
