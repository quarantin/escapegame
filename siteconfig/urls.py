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
from django.urls import include, path
from django.contrib.auth.views import LoginView
from escapegame import views

urlpatterns = [
	# Landing page
	path('', views.index),

	# Authentication
	path('accounts/', include('django.contrib.auth.urls')),

	# Admin section
	path('admin/', admin.site.urls),

	# Challenge status module
	path('challenge/', include('challenge.urls')),

	# Door module
	#path('door/', include('door.urls')),

	# Escape game section
	path('escapegame/', include('escapegame.urls')),

	# Video module
	#path('video/', include('video.urls')),
]
