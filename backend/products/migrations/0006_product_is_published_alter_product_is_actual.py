# Generated by Django 5.2.1 on 2025-06-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_options_alter_manufacturer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Если задан, товар будет отображаться на сайте', verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_actual',
            field=models.BooleanField(default=True, help_text='Если задан, значит был успешно загружен при последнем импорте', verbose_name='Актуальна'),
        ),
    ]
