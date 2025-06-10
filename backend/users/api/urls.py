from rest_framework.routers import DefaultRouter

from .views import CustomerBotViewSet

router = DefaultRouter()
router.register('bot-customers', CustomerBotViewSet)

urlpatterns = router.urls
