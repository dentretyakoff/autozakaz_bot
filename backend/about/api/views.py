from rest_framework import mixins, viewsets

from about.models import Contact, GDPR
from .serializers import ContactSerializer, GDPRSerializer


class ContactViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.filter(is_actual=True)
    serializer_class = ContactSerializer


class GDPRViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GDPR.objects.filter(is_actual=True)
    serializer_class = GDPRSerializer
