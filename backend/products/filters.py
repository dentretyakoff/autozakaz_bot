import django_filters
from django import forms
from django.db.models import Q

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
        qs = queryset.filter(
            Q(code__iexact=value.upper()) |
            Q(product_code__iexact=value.upper())
        )
        documents = []
        for p in qs:
            doc = p.meili_serialize() | {'id': str(p.pk), 'pk': str(p.pk)}
            documents.append(doc)
        if documents:
            Product.meilisearch.index.add_documents(documents)
        return qs

    def filter_meilisearch(self, queryset, name, value):
        return Product.meilisearch.search(value).filter(is_published=True)
