from django.contrib import admin, messages
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone

from base.admin import TimeStampedAdmin
from .models import CSVPrice, ImportTask, CSVColumn, WordToDrop
from .tasks import import_goods


@admin.register(CSVColumn)
class CSVColumnAdmin(TimeStampedAdmin):
    list_display = ('name', 'drop_by_words')


@admin.register(WordToDrop)
class WordToDropAdmin(TimeStampedAdmin):
    list_display = ('word',)
    search_fields = ('name',)


@admin.register(CSVPrice)
class CSVPriceAdmin(TimeStampedAdmin):
    list_display = (
        'name',
        'url',
        'period_min',
        'new_period_min',
        'price_filter',
    )
    filter_horizontal = ('ignored_manufacturers',)


@admin.register(ImportTask)
class ImportTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'active',
        'run_at',
        'scheduled_at',
        'last_run',
        'run_now_button',
    )
    readonly_fields = ('scheduled_at', 'last_run')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('active',)
    filter_horizontal = ('prices',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:task_id>/run-now/',
                 self.admin_site.admin_view(self.run_now_view),
                 name='importtask_run_now'),
        ]
        return custom_urls + urls

    def run_now_button(self, obj):
        return format_html(
            '<a class="button" style="padding:2px 5px;background:#28a745;color:white;border-radius:3px;" href="{}">Запустить</a>',  # noqa
            f'{obj.id}/run-now/'
        )
    run_now_button.short_description = 'Ручной запуск'

    def run_now_view(self, request, task_id):
        task = get_object_or_404(ImportTask, pk=task_id)
        import_goods.delay(task.id)
        task.scheduled_at = timezone.localtime()
        task.save(update_fields=['scheduled_at'])
        self.message_user(
            request,
            f"Задача '{task.name}' поставлена в очередь Celery.",
            level=messages.SUCCESS
        )
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))
