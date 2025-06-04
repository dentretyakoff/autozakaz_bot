from django_filters.views import FilterView
from django.conf import settings

from .models import Product
from .filters import ProductFilter


class Products(FilterView):
    """Список товаров."""
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = settings.PAGINATE_BY
    filterset_class = ProductFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = query_params.urlencode()
        return context
