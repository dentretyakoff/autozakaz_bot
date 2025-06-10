from rest_framework import mixins, viewsets

from about.models import Contact
from .serializers import ContactSerializer


class ContactViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.filter(is_actual=True)
    serializer_class = ContactSerializer
