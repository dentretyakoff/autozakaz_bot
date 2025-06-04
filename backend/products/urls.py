from django.urls import path

from .views import Products


app_name = 'products'

urlpatterns = [
    path('', Products.as_view(), name='products'),
]
