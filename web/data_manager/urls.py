"""data_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.shortcuts import redirect
from django.urls import include, path
from . import settings, views
from django.urls import re_path

urlpatterns = [
    # block user direct access to database folder
    re_path(r'^files/primary_storage/database/(?P<path>.*)',
            views.contact,
            name="contact"),
    path('admin/', admin.site.urls),
    path('files/', include('file_manager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name="sign-up"),
    path('contact/', views.contact, name="contact"),
    path('', lambda req: redirect('/files/'), name='home'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
