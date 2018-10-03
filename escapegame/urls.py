# -*- coding: utf-8 -*-

from django.urls import path

from . import views


urlpatterns = [

	################
	# Web Frontend #
	################

	# Escape game index view
	path('', views.escapegame_index),

	# Used to check host connectivity
	path('ping/', views.escapegame_ping),

	# Escape game detail view
	path('<slug:game_slug>/', views.escapegame_detail),

	# Escape game controls
	path('<slug:game_slug>/reset/', views.escapegame_reset),
	path('<slug:game_slug>/status/', views.escapegame_status),

	############
	# REST API #
	############

	# Challenge controls
	path('api/challenge/<slug:game_slug>/<slug:room_slug>/<slug:challenge_slug>/<str:action>/', views.rest_challenge_control),

	# Door controls
	path('api/door/<slug:game_slug>/<slug:room_slug>/<slug:door_slug>/<str:action>/', views.rest_door_control),

	# Lift controls
	path('api/lift/<slug:game_slug>/<slug:lift_slug>/<str:action>/', views.rest_lift_control),

	# Video controls
	path('api/video/<slug:media_slug>/<str:action>/', views.rest_media_control),
]
