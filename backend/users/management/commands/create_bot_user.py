import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    """Создание пользователя для бота."""
    help = 'Создание пользователя для бота'

    def handle(self, *args, **kwarg):
        user_model = get_user_model()
        username = os.getenv('BOT_USER')
        password = os.getenv('BOT_PASSWORD')
        email = os.getenv('BOT_EMAIL')
        if not username or not password or not email:
            self.stdout.write(
                self.style.ERROR(
                    'Заполни данные для создания пользователя '
                    'для бота в файле .env'))
            return
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            user = user_model.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            self.stdout.write(
                self.style.SUCCESS('Создан пользователь бота.'))
        token, _ = Token.objects.get_or_create(user=user)
        self.stdout.write(
                self.style.SUCCESS(f'Токен: {token}'))
