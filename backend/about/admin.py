from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Contact, Oferta


@admin.register(Contact)
class ContactAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'requisites',
        'address',
        'phone',
        'email',
        'is_actual'
    )
    list_display_links = ('id', 'requisites')


@admin.register(Oferta)
class OfertaAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'name',
        'is_actual'
    )
    list_display_links = ('id', 'name')
