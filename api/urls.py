# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [

	# Configuration
	path('config', views.set_config),

	# Door controls
	path('door/<str:action>/<int:pin>/', views.set_door_locked),
]
