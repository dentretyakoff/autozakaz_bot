from .users import UsersApi
from .about import AboutApi
from .products import ProductsApi


class APIBackend:
    def __init__(self):
        self.users = UsersApi()
        self.about = AboutApi()
        self.products = ProductsApi()


api_backend = APIBackend()
