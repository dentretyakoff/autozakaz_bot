from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API
    path(f'api/{settings.API_VERSION}/users/', include('users.api.urls')),
    path(
        f'api/{settings.API_VERSION}/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        f'api/{settings.API_VERSION}/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    # Apps
    path('', include('products.urls', namespace='products')),
    path('', include('about.urls', namespace='about'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
