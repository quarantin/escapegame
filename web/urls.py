# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [

	#####
	# Web API
	#####

	# Escape game selector view
	path('', views.selector_index, name='Index'),

	# Escape game control view
	path('<slug:game_slug>/', views.escapegame_index),

	# Escape game controls
	path('<slug:game_slug>/start/', views.escapegame_start),
	path('<slug:game_slug>/reset/', views.escapegame_reset),
	path('<slug:game_slug>/status/', views.escapegame_status),

	# Video controls
	path('<slug:game_slug>/video/<str:action>/', views.set_video_state),

	# Door controls
	path('<slug:game_slug>/<slug:room_slug>/<str:action>/', views.set_door_locked),

	# Challenge controls
	path('<slug:game_slug>/<slug:room_slug>/<slug:challenge_slug>/<str:action>/', views.set_challenge_status),
]
