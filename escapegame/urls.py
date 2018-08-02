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
	path('<slug:game_slug>/', views.escapegame_index, name='Escape game index'),
	path('<slug:game_slug>/start/', views.escapegame_start, name='Start escape game'),
	path('<slug:game_slug>/reset/', views.escapegame_reset, name='Reset escape game'),
	path('<slug:game_slug>/status/', views.escapegame_status, name='Escape game status'),

	#####
	# REST API
	#####

	# Video controls
	path('<slug:game_slug>/video/<str:action>/', views.set_video_state, name='Play/stop briefing video'),

	# Door controls
	path('<slug:game_slug>/door/<slug:room_slug>/<str:action>/', views.set_door_lock, name='Lock/unlock doors'),

	# Challenge controls
	path('<slug:game_slug>/challenge/<slug:challenge_slug>/<str:action>/', views.set_challenge_status, name='Solve/reset challenges'),
]
