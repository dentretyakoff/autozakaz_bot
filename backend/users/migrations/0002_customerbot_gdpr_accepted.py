# Generated by Django 5.2.1 on 2025-06-15 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbot',
            name='gdpr_accepted',
            field=models.BooleanField(default=False, help_text='Статус согласия на обработку перс. данных', verbose_name='Согласие на ПД'),
        ),
    ]
