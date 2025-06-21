from .users import UsersApi
from .about import AboutApi
from .products import ProductsApi
from .orders import OrdersApi


class APIBackend:
    def __init__(self):
        self.users = UsersApi()
        self.about = AboutApi()
        self.products = ProductsApi()
        self.orders = OrdersApi()


api_backend = APIBackend()
