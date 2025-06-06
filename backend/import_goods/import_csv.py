import os
import logging
from decimal import Decimal

import wget
import pandas as pd
import numpy as np
from pandas import DataFrame
from django.conf import settings
from django.db import transaction

from products.models import Manufacturer, Product, PriceMarkup
from .models import CSVPrice, CSVColumn, WordToDrop
from .constansts import (
    COLUMNS_SORT,
    COLUMNS_DUPLICATES,
    COLUMN_MANUFACTURER,
    COLUMN_CODE,
    COLUMN_NAME,
    COLUMN_DESCRIPTION,
    COLUMN_PRICE,
    COLUMN_PERIOD_MIN,
)

logger = logging.getLogger(__name__)


class CSVImport:
    def __init__(self, csv_price: CSVPrice):
        self.csv_price = csv_price
        self.url = csv_price.url
        self.markups = list(PriceMarkup.objects.all())

    def import_csv(self) -> None:
        """Основной метод для скачивания и загрузки в БД прайс-листа."""
        self.csv_price.products.all().update(is_actual=False)
        csv_file = wget.download(
            self.url, out=str(settings.TEMP_DIR), bar=None)
        df = pd.read_csv(
            csv_file, sep=';', low_memory=False, header=0, encoding='cp1251')
        df.sort_values(COLUMNS_SORT, inplace=True)
        df.drop_duplicates(
            subset=COLUMNS_DUPLICATES, keep='first', inplace=True)

        df = df.loc[(df[COLUMN_PERIOD_MIN] >= self.csv_price.period_min)]
        if self.csv_price.new_period_min:
            df[COLUMN_PERIOD_MIN] = self.csv_price.new_period_min
        if self.csv_price.price_filter:
            df = df.loc[df[COLUMN_PRICE] >= self.csv_price.price_filter]

        ignored = set(self.csv_price.ignored_manufacturers.values_list('name', flat=True))  # noqa
        df = df[~df[COLUMN_MANUFACTURER].isin(ignored)]

        df = self.drop_by_words(df)
        self.create_in_db(df)
        os.remove(csv_file)

    def drop_by_words(self, df: DataFrame) -> DataFrame:
        columns = list(CSVColumn.objects.filter(drop_by_words=True)
                       .values_list('name', flat=True))
        words = list(WordToDrop.objects.all().values_list('word', flat=True))
        if columns and words:
            df = df[~df[columns].apply(
                lambda x: x.str.contains('|'.join(words))).any(
                axis=1)]

        return df

    def increase_price(self, price: float) -> int:
        if price is None:
            return 0

        percent = 0

        for markup in self.markups:
            if price <= markup.threshold:
                percent = markup.percent
                break
        else:
            if self.markups:
                percent = self.markups[-1].percent

        new_price = Decimal(price) * (1 + Decimal(percent) / 100)
        return int(round(new_price))

    def create_in_db(self, df: DataFrame) -> None:
        """Создает производителей и продукты. bulk_create, bulk_update"""
        df.replace({np.nan: None}, inplace=True)

        manufacturer_names = df[COLUMN_MANUFACTURER].dropna().unique()
        existing_manufacturers = self.create_manufacturers(manufacturer_names)
        existing_products = {
           (p.manufacturer.id, p.code, p.csv_price.id): p
           for p in Product.objects.filter(csv_price=self.csv_price)
        }
        to_create, to_update = self.prepare_products(
            df, existing_manufacturers, existing_products)

        with transaction.atomic():
            if to_create:
                created_products = Product.objects.bulk_create(
                    to_create, batch_size=1000)
                for product in created_products:
                    product.product_code = product.id_to_base36(product.id)
                Product.objects.bulk_update(
                    created_products, ['product_code'], batch_size=1000)
            logger.info(f'Новых продуктов: {len(to_create)}')
            if to_update:
                Product.objects.bulk_update(
                    to_update,
                    ['name', 'description', 'price', 'period_min', 'is_actual'],  # noqa
                    batch_size=1000)
            logger.info(f'Обновлено продуктов: {len(to_update)}')

    def create_manufacturers(
            self,
            manufacturer_names: str) -> dict[str, Manufacturer]:
        """Создает производителей - bulk_create."""
        manufacturers = {
            m.name: m
            for m in Manufacturer.objects.filter(name__in=manufacturer_names)}
        missing = set(manufacturer_names) - set(manufacturers.keys())
        new_manufacturers = [Manufacturer(name=name) for name in missing]
        logger.info(f'Новых производителей: {len(new_manufacturers)}')
        Manufacturer.objects.bulk_create(new_manufacturers)
        manufacturers.update(
            {m.name: m for m in Manufacturer.objects.filter(name__in=missing)})
        logger.info(f'Всего производителей: {len(manufacturers)}')

        return manufacturers

    def prepare_products(
            self,
            df: DataFrame,
            existing_manufacturers: dict,
            existing_products: dict) -> tuple[list, list]:
        """Подготавливает списки продуктов на создание и обновление."""
        to_create = []
        to_update = []

        for row in df.to_dict(orient='records'):
            manufacturer = existing_manufacturers[row[COLUMN_MANUFACTURER]]
            key = (manufacturer.id, row[COLUMN_CODE], self.csv_price.id)

            defaults = {
                'name': row[COLUMN_NAME],
                'description': row[COLUMN_DESCRIPTION],
                'price': self.increase_price(row[COLUMN_PRICE]),
                'period_min': row[COLUMN_PERIOD_MIN],
                'is_actual': True
            }

            if key in existing_products:
                product = existing_products[key]
                for field, value in defaults.items():
                    setattr(product, field, value)
                to_update.append(product)
            else:
                product = Product(
                    manufacturer=manufacturer,
                    code=row[COLUMN_CODE],
                    csv_price=self.csv_price,
                    **defaults)
                to_create.append(product)

        return to_create, to_update
