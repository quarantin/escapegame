# -*- coding: utf-8 -*-

from django.urls import path
from . import views


urlpatterns = [

	#####
	# Web Frontend
	#####

	# Escape game index view
	path('', views.escapegame_index),

	# Escape game detail view
	path('<slug:game_slug>/', views.escapegame_detail),

	# Escape game controls
	path('<slug:game_slug>/pause/', views.escapegame_pause),
	path('<slug:game_slug>/start/', views.escapegame_start),
	path('<slug:game_slug>/reset/', views.escapegame_reset),
	path('<slug:game_slug>/status/', views.escapegame_status),
]
