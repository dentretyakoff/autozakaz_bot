import django_filters
from django import forms
from django.db.models import Q

from import_goods.import_handlers.import_api import APIImport
from .models import Product


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_all',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск детали...'
        })
    )
    search_bot = django_filters.CharFilter(
        method='filter_by_code',
        label='',
    )
    meilisearch = django_filters.CharFilter(
        method='filter_meilisearch',
        label='',
    )

    class Meta:
        model = Product
        fields = []

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(name__startswith=value) |
            Q(code__iexact=value.upper()) |
            Q(product_code__iexact=value.upper()) |
            Q(manufacturer__name__iexact=value)
        )

    def filter_by_code(self, queryset, name, value):
        api_import = APIImport()
        qs = queryset.filter(
            Q(code__iexact=value.upper()) |
            Q(product_code__iexact=value.upper())
        )
        updated_qs = api_import.update_products(qs)
        self._update_meilisearch(updated_qs)
        return updated_qs

    def _update_meilisearch(self, qs):
        documents = []
        for p in qs:
            doc = p.meili_serialize() | {'id': str(p.pk), 'pk': str(p.pk)}
            documents.append(doc)
        if documents:
            Product.meilisearch.index.add_documents(documents)

    def filter_meilisearch(self, queryset, name, value):
        return Product.meilisearch.search(value).filter(is_published=True)
