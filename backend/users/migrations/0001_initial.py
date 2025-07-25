# Generated by Django 5.2.1 on 2025-06-10 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('telegram_id', models.PositiveBigIntegerField(unique=True, verbose_name='Телеграм ID')),
                ('nickname', models.CharField(blank=True, max_length=255, null=True, verbose_name='Никнейм')),
            ],
            options={
                'verbose_name': 'Клиент бота',
                'verbose_name_plural': 'Клиенты бота',
            },
        ),
    ]
