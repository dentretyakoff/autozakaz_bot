from rest_framework import mixins, viewsets

from about.models import Contact
from .serializers import ContactSerializer


class ContactViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
