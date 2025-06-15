from rest_framework.routers import DefaultRouter

from .views import ContactViewSet, GDPRViewSet

router = DefaultRouter()
router.register('contacts', ContactViewSet)
router.register('gdpr', GDPRViewSet)

urlpatterns = router.urls
