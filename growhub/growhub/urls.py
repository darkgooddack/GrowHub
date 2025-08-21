import base64
from functools import wraps

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from growhub.settings import SWAGGER_PASSWORD, SWAGGER_USER


def swagger_password_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            auth_method, auth = auth_header.split(' ', 1)
            if auth_method.lower() == 'basic':
                decoded_auth = base64.b64decode(auth).decode('utf-8')
                username, password = decoded_auth.split(':', 1)
                if username == SWAGGER_USER and password == SWAGGER_PASSWORD:
                    return view_func(request, *args, **kwargs)
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Swagger"'
        return response
    return _wrapped_view


schema_view = get_schema_view(
    openapi.Info(
        title='GrowHub',
        default_version='v1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('projects.urls')),
    path('swagger/', swagger_password_required(
        schema_view.with_ui('swagger', cache_timeout=0)
    ), name='schema-swagger-ui'),
]

