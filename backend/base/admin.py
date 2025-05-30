from django.contrib import admin
from django.conf import settings


class TimeStampedAdmin(admin.ModelAdmin):
    base_readonly_fields = ('created_at', 'updated_at')
    base_list_display = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = getattr(self, 'readonly_fields', ())
        return readonly_fields + self.base_readonly_fields

    def get_list_display(self, request):
        list_display = getattr(self, 'list_display', ())
        return list_display + self.base_readonly_fields


project_name = settings.PROJECT_NAME
admin.site.site_header = f'Панель управления {project_name}'
admin.site.site_title = f'Панель управления {project_name}'
