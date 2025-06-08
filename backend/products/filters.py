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
