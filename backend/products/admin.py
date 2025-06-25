from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Manufacturer, Product, PriceMarkup


@admin.register(Manufacturer)
class ManufacturerAdmin(TimeStampedAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    readonly_fields = ('id',)
    search_fields = ('name',)


@admin.action(description='Опубликовать выбранные')
def publish_selected(modeladmin, request, queryset):
    updated = 0
    for obj in queryset:
        if not obj.is_published:
            obj.is_published = True
            obj.save()
            updated += 1
    modeladmin.message_user(request, f'Опубликовано {updated} объектов.')


@admin.action(description='Снять с публикации')
def unpublish_selected(modeladmin, request, queryset):
    updated = 0
    for obj in queryset:
        if obj.is_published:
            obj.is_published = False
            obj.save()
            updated += 1
    modeladmin.message_user(request, f'Снято с публикации {updated} объектов.')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_code',
        'name',
        'manufacturer',
        'code',
        'price',
        'period_min',
        'is_published'
    )
    readonly_fields = (
        'id',
        'manufacturer',
        'code',
        'product_code',
        'period_min',
    )
    list_display_links = ('name',)
    search_fields = (
        'id',
        'code',
        'product_code'
    )
    list_filter = ('is_published',)
    actions = [publish_selected, unpublish_selected]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PriceMarkup)
class PriceMarkupAdmin(TimeStampedAdmin):
    list_display = ('id', 'threshold', 'percent')
    list_display_links = ('threshold',)
