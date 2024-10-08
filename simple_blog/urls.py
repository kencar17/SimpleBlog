"""simple_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from simple_blog import settings

urlpatterns = [
    path("blog-site-admin", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/auth/", include("apps.authentication.urls")),
    path("api/", include("apps.account.urls")),
    path("api/", include("apps.blog.urls")),
    path("api/", include("apps.comments.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
