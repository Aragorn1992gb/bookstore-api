"""
URL configuration for bookstore_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from bookstore_api.admin import admin_site
from django.urls import path, include, re_path
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import BasicAuthentication
from dj_rest_auth.views import PasswordResetConfirmView

schema_view = get_schema_view(
   openapi.Info(
      title="BOOKSTORE API",
      default_version='v1',
      description="BOOKSTORE API",
   ),
   public=True,
   authentication_classes=(BasicAuthentication,),
)

admin.site.site_header = 'Bookstore API Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls'), name='book'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
