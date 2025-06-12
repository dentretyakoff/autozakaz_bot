from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import CustomerBot


@admin.register(CustomerBot)
class CustomerBotAdmin(TimeStampedAdmin):
    list_display = ('id', 'telegram_id', 'nickname')
    list_display_links = ('name',)
    readonly_fields = ('id',)
    search_fields = ('name',)
