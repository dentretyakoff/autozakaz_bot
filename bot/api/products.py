from .base import APIClientBase


class ProductsApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/products'

    def search_products(self, query: str, meilisearch: bool = False) -> list:
        q = 'search'
        if meilisearch:
            q = 'meilisearch'
        response = self._get(f'/products/?{q}={query}')
        results = response.json()['results']
        return results

    def get_product(self, pk: int) -> dict:
        response = self._get(f'/products/{pk}')
        return response.json()
