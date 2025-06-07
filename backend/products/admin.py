from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Manufacturer, Product, PriceMarkup


@admin.register(Manufacturer)
class ManufacturerAdmin(TimeStampedAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    readonly_fields = ('id',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_code',
        'name',
        'manufacturer',
        'code',
        'price',
        'period_min',
        'is_actual',
    )
    readonly_fields = (
        'id',
        'manufacturer',
        'code',
        'product_code',
        'name',
        'period_min',
        'csv_price',
    )
    list_display_links = ('name',)
    search_fields = (
        'id',
        'name',
        'code',
        'manufacturer__name',
        'product_code'
    )
    list_filter = ('is_actual',)


@admin.register(PriceMarkup)
class PriceMarkupAdmin(TimeStampedAdmin):
    list_display = ('id', 'threshold', 'percent')
    list_display_links = ('threshold',)
