from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Devops Thug Life API's",
        default_version='v1',
        description="Nir elmaliah Fullstack Projects",
        contact=openapi.Contact(email="nirprime@outlook.com"),  
        license=openapi.License(name="MIT License"),
    ),
    public=True,

)

urlpatterns = [
     path('admin/', admin.site.urls),
     path('', include('myapp.apis.urls')),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]