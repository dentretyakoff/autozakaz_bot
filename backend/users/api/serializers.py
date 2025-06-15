from rest_framework import serializers

from users.models import CustomerBot


class CustomerBotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBot
        fields = ('telegram_id', 'nickname')


class CustomerBotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBot
        fields = ('nickname', 'gdpr_accepted')


class CustomerBotRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBot
        fields = ('id', 'telegram_id', 'nickname', 'gdpr_accepted')
