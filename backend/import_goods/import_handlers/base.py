from decimal import Decimal

from products.models import PriceMarkup


class ImportBase:
    def __init__(self):
        self.markups = list(PriceMarkup.objects.all())

    def increase_price(self, price: float) -> int:
        """Производит наценку в зависимости от порога."""
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
