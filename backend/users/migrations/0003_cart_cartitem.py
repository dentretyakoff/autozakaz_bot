# Generated by Django 5.2.1 on 2025-06-18 08:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_is_published_alter_product_is_actual'),
        ('users', '0002_customerbot_gdpr_accepted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('payment_method', models.CharField(choices=[('cash', 'Наличные'), ('card', 'Карта'), ('robokassa', 'Робокасса')], default='robokassa', max_length=10, verbose_name='Способ оплаты')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Комментарий для заказа')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='users.customerbot', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Количество')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='users.cart', verbose_name='Клиент')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cartitems', to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар корзины',
                'verbose_name_plural': 'Товары корзин',
            },
        ),
    ]
