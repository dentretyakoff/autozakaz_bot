from django.conf import settings


def project_name(request):
    """Добавляет переменную с именем проекта."""
    return {
        'project_name': settings.PROJECT_NAME
    }
