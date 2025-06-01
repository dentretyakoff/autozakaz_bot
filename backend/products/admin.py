from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Manufacturer, Product, PriceMarkup


@admin.register(Manufacturer)
class ManufacturerAdmin(TimeStampedAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'manufacturer',
        'code',
        'product_code',
        'name',
        'price',
        'period_min',
        'is_actual',
    )
    readonly_fields = (
        'manufacturer',
        'code',
        'product_code',
        'name',
        'period_min',
        'csv_price',
    )
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code', 'manufacturer__name')
    list_filter = ('is_actual',)


@admin.register(PriceMarkup)
class PriceMarkupAdmin(TimeStampedAdmin):
    list_display = ('id', 'threshold', 'percent')
