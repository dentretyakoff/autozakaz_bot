from django.urls import path

from .views import ContactsView, OfertaView


app_name = 'about'

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('oferta/', OfertaView.as_view(), name='oferta'),
]
