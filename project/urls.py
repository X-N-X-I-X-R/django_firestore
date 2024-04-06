from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API for my Django project",
    ),
    public=True,
)

urlpatterns = [
     path('admin/', admin.site.urls),
     path('', include('myapp.urls')),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


'''
http://127.0.0.1:8000/swagger/

'''