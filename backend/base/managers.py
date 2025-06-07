from django.contrib.contenttypes.models import ContentType
from django.db import models


class SpecificContentTypeManager(models.Manager):
    def __init__(self, model_for_filter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_for_filter = model_for_filter

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(self.model_for_filter)
        return super().get_queryset().filter(content_type=content_type)


def get_specific_content_type_manager(model_for_filter):
    class _SpecificContentTypeManager(SpecificContentTypeManager):
        def __init__(self):
            super().__init__(model_for_filter=model_for_filter)
    return _SpecificContentTypeManager()
