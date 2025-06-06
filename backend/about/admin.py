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
    list_display_links = ('requisites',)
    readonly_fields = ('id',)


@admin.register(Oferta)
class OfertaAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'name',
        'oferta_file',
        'is_actual'
    )
    list_display_links = ('name',)
    readonly_fields = ('id',)
