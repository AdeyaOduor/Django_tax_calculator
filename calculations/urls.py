# for calculations views
from django.urls import path
from .views import calculate_tax
from . import views

urlpatterns = [
    path('calculations/', views.calculate_tax, name='calculate_tax'),
    path('', calculate_tax, name='calculate_tax'),
    # Add other URLs as needed
]