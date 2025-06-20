# Generated by Django 5.2.1 on 2025-06-07 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('import_goods', '0002_initial'),
        ('products', '0003_alter_product_options'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('manufacturer', 'code', 'csv_price'), name='unique_product_per_csv'),
        ),
    ]
