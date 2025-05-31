from django.contrib import admin

from base.admin import TimeStampedAdmin
from .models import CSVPrice, ImportTask


@admin.register(CSVPrice)
class CSVPriceAdmin(TimeStampedAdmin):
    list_display = ('name', 'url')


@admin.register(ImportTask)
class ImportTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'active',
        'run_at',
        'scheduled_at',
        'last_run',
    )
    readonly_fields = ('scheduled_at', 'last_run')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('active',)
    filter_horizontal = ('prices',)
