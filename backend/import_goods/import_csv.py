import os
import logging
from decimal import Decimal

import wget
import pandas as pd
import numpy as np
from pandas import DataFrame
from django.conf import settings

from products.models import Manufacturer, Product, PriceMarkup
from base.enums import LogLevel
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

    def download_file(self):
        self.csv_file = wget.download(
            self.url, out=str(settings.TEMP_DIR), bar=None)

    def prepare_csv(self) -> DataFrame:
        self.csv_price.products.all().update(is_actual=False)
        df = pd.read_csv(self.csv_file, sep=';', low_memory=False,
                         header=0, encoding='cp1251')
        df.sort_values(COLUMNS_SORT, inplace=True)
        df.drop_duplicates(
            subset=COLUMNS_DUPLICATES, keep='first', inplace=True)
        df = df.dropna(subset=[COLUMN_MANUFACTURER, COLUMN_CODE, COLUMN_NAME])

        df = df.loc[(df[COLUMN_PERIOD_MIN] >= self.csv_price.period_min)]
        if self.csv_price.new_period_min:
            df[COLUMN_PERIOD_MIN] = self.csv_price.new_period_min
        if self.csv_price.price_filter:
            df = df.loc[df[COLUMN_PRICE] >= self.csv_price.price_filter]

        ignored = set(self.csv_price.ignored_manufacturers.values_list('name', flat=True))  # noqa
        df = df[~df[COLUMN_MANUFACTURER].isin(ignored)]

        df = self.drop_by_words(df)
        df.replace({np.nan: None}, inplace=True)

        return df

    def import_csv(self) -> None:
        """Основной метод для скачивания и загрузки в БД прайс-листа."""
        try:
            self.download_file()
            df = self.prepare_csv()
            self.create_in_db(df)
            self.update_product_codes()
        except Exception as e:
            message = f'{self.csv_price} - Ошибка импорта: {e}'
            logger.error(message)
            self.csv_price.logs.create(
                level=LogLevel.ERROR,
                message=message
            )
            raise
        finally:
            if self.csv_file:
                os.remove(self.csv_file)

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
        self.create_manufacturers(df[COLUMN_MANUFACTURER].dropna().unique())
        self.create_products(df)

    def create_manufacturers(self, manufacturer_names: str) -> None:
        """Создает производителей - bulk_create."""
        message = f'{self.csv_price} - Создаем производителей'
        logger.info(message)
        self.csv_price.logs.create(level=LogLevel.INFO, message=message)
        manufacturers = [
            Manufacturer(name=name) for name in manufacturer_names
        ]
        Manufacturer.objects.bulk_create(
            manufacturers,
            ignore_conflicts=True,
            batch_size=1000
        )

    def create_products(self, df: DataFrame):
        products = []
        manufacturers = dict(
            Manufacturer.objects.values_list('name', 'id')
        )
        message = f'{self.csv_price} - Подготавливаем товары'
        logger.info(message)
        self.csv_price.logs.create(level=LogLevel.INFO, message=message)
        for row in df.to_dict(orient='records'):
            try:
                products.append(
                    Product(
                        manufacturer_id=manufacturers[row[COLUMN_MANUFACTURER]],  # noqa
                        code=row[COLUMN_CODE],
                        csv_price=self.csv_price,
                        name=row[COLUMN_NAME],
                        description=row[COLUMN_DESCRIPTION],
                        price=self.increase_price(row[COLUMN_PRICE]),
                        period_min=row[COLUMN_PERIOD_MIN],
                        is_actual=True,
                    )
                )
            except Exception as e:
                message = f'{self.csv_price} - Ошибка подготовки товара - {row}{e}'  # noqa
                logger.error(message)
                self.csv_price.logs.create(
                    level=LogLevel.ERROR, message=message)
        message = f'{self.csv_price} - Создаем товары {len(products)}'
        logger.info(message)
        self.csv_price.logs.create(level=LogLevel.INFO, message=message)
        Product.objects.bulk_create(
            products,
            batch_size=5000,
            update_conflicts=True,
            unique_fields=('manufacturer', 'code', 'csv_price'),
            update_fields=('description', 'price', 'period_min', 'is_actual')
        )

    def update_product_codes(self, batch_size=100_000):
        """
        Постепенно обновляет product_code для всех продуктов, где он пустой.
        """
        total_updated = 0

        while True:
            qs = (
                Product.objects
                .filter(product_code__isnull=True)
                .only('id', 'product_code')
                .order_by('id')
            )
            batch = list(qs[:batch_size])
            if not batch:
                break

            for product in batch:
                product.product_code = product.id_to_base36(product.id)

            Product.objects.bulk_update(
                batch, ['product_code'], batch_size=5000)
            total_updated += len(batch)
            message = (
                f'{self.csv_price} - Обновлено product_code: {len(batch)} '
                f'(всего: {total_updated})'
            )
            logger.info(message)
            self.csv_price.logs.create(level=LogLevel.INFO, message=message)
