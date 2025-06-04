from django.views.generic.base import TemplateView

from .models import Contact, Oferta


class ContactsView(TemplateView):
    """Список товаров."""
    template_name = 'about/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.filter(is_actual=True).first()
        return context


class OfertaView(TemplateView):
    """Оферта."""
    template_name = 'about/oferta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['oferta'] = Oferta.objects.filter(is_actual=True).first()
        return context
