from rest_framework.routers import DefaultRouter

from .views import CustomerBotViewSet, CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register('bot-customers', CustomerBotViewSet)
router.register('cart', CartViewSet)
router.register('cart-items', CartItemViewSet)

urlpatterns = router.urls
