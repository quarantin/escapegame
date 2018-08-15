# -*- coding: utf-8 -*-

"""escapegame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView

from escapegame import admin as myadmin

urlpatterns = [

	# Landing page
	path('', RedirectView.as_view(url='/web/', permanent=False)),

	# Authentication pages
	path('accounts/', include('django.contrib.auth.urls')),

	# Escape games admin pages
	path('admin/', myadmin.site.urls),

	# Django admin pages
	path('admin/django/', admin.site.urls),

	# JSON Import / Export admin pages
	path('admin/json/', include('jsonexport.urls')),

	# REST API (slave)
	path('api/', include('api.urls')),

	# Web interface
	path('web/', include('web.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
