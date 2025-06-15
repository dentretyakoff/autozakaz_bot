from rest_framework import serializers

from about.models import Contact, GDPR


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'requisites',
            'address',
            'phone',
            'email'
        )


class GDPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = GDPR
        fields = (
            'id',
            'name',
            'text',
            'is_actual'
        )
