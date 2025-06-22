from django.urls import path
from .views import robokassa_redirect


app_name = 'orders'


urlpatterns = [
    path('pay/<str:token>/', robokassa_redirect, name='robokassa_redirect'),
]
