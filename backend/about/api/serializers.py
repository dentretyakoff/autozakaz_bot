from rest_framework import serializers

from about.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'requisites',
            'address',
            'phone',
            'email'
        )
