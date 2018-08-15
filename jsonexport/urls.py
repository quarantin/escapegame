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

from . import views

urlpatterns = [

	# JSON Import/Export index
	path('', views.json_index, name='json_index'),

	# JSON Export
	path('export/', views.json_export, name='json_export'),

	# JSON Import
	path('import/', views.json_import, name='json_import'),

]
