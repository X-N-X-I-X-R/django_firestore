from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from myapp.views.swagger_view import SwaggerLoginView, staff_member_required
from rest_framework.authentication import SessionAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Django Server API",
        default_version='v1',
        description="API documentation for Django Server",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@djangoserver.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
    authentication_classes=[SessionAuthentication],
    url=f"{settings.BASE_URL}/api/v1" if hasattr(settings, 'BASE_URL') else None,
)

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
    
    # Swagger URLs with proper authentication
    path('swagger/login/', SwaggerLoginView.as_view(), name='swagger-login'),
    path('swagger<format>/', staff_member_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    path('swagger/', staff_member_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', staff_member_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    
    

