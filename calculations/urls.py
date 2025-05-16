# calculations/urls.py
from django.urls import path
from .views import calculate_tax

urlpatterns = [
    path('', calculate_tax, name='calculate_tax'),
]