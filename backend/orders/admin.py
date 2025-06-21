from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'product_price', 'quantity')
    readonly_fields = ('product', 'product_price', 'quantity')
    can_delete = False
    max_num = 0

    def product_price(self, obj):
        return f'{obj.product.price} ₽' if obj.product else None
    product_price.short_description = 'Цена товара'


@admin.register(Order)
class OrderAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'customer',
        'customer_phone',
        'status',
        'payment_method',
        'total_price_display',
        'expiration_date',
    )
    readonly_fields = (
        'customer',
        'customer_phone',
        'payment_method',
        'total_price_display',
        'comment',
        'expiration_date',
        'status'
    )
    list_display_links = ('id', 'customer')
    search_fields = (
        'id',
        'customer__telegram_id',
        'customer__nickname',
        'customer__phone',
    )
    list_filter = (
        'status',
    )
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def total_price_display(self, obj):
        return f'{obj.total_price} ₽'
    total_price_display.short_description = 'Общая сумма'

    def customer_phone(self, obj):
        return obj.customer.phone if obj.customer else '-'
    customer_phone.short_description = 'Телефон клиента'
