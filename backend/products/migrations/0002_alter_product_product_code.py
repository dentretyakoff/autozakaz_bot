# Generated by Django 5.2.1 on 2025-06-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Артикул товара'),
        ),
    ]
