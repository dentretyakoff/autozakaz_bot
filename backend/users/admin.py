from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import CustomerBot, Cart, CartItem


@admin.register(CustomerBot)
class CustomerBotAdmin(TimeStampedAdmin):
    list_display = ('id', 'telegram_id', 'nickname', 'gdpr_accepted')
    list_display_links = ('name',)
    readonly_fields = ('id', 'gdpr_accepted')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'product_price', 'quantity')
    readonly_fields = ('product', 'product_price', 'quantity')
    can_delete = False
    max_num = 0

    def product_price(self, obj):
        return f'{obj.product.price} ₽' if obj.product else None
    product_price.short_description = 'Цена товара'


@admin.register(Cart)
class CartAdmin(TimeStampedAdmin):
    list_display = (
        'id',
        'customer',
        'payment_method',
        'comment',
        'total_price_display',
    )
    list_display_links = ('id', 'customer')
    readonly_fields = (
        'customer',
        'payment_method',
        'comment',
        'total_price_display',
    )
    inlines = [CartItemInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def total_price_display(self, obj):
        return f'{obj.total_price} ₽'
    total_price_display.short_description = 'Общая сумма'
