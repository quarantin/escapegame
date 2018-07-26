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
from django.urls import include, path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
	# Landing page
	path('', views.index),

	# Admin section
	path('admin/', admin.site.urls),

	# Authentication
	path('accounts/', include('django.contrib.auth.urls')),

	# Door module
	path('door/', include('door.urls')),

	# Status module
	path('status/', include('status.urls')),

	# Video module
	path('video/', include('video.urls')),

	# 1001 nuits module
	path('1001-nuits/', include('mille_et_une_nuits.urls')),

	# Stranger things module
	path('stranger-things/', include('stranger_things.urls')),
]
