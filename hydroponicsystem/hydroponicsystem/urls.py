from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Hydroponic systems miniproject API Documentation",
        default_version="v1",
        description="API docs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]