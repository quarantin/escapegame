# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [

	# Escape game selector view
	path('', views.index, name='Index'),

	# Escape game control view
	path('<slug:game_slug>/', views.escapegame, name='Escape Game'),
	path('<slug:game_slug>/start/', views.escapegame_start, name='Start Escape Game'),
	path('<slug:game_slug>/reset/', views.escapegame_reset, name='Reset Escape Game'),

	# Video controls
	path('<slug:game_slug>/video/play/', views.video_play, name='Play Brief Video'),
	path('<slug:game_slug>/video/stop/', views.video_stop, name='Stop Brief Video'),

	# Door controls
	path('<slug:game_slug>/door/<slug:room_slug>/', views.door_status, name='Door Status'),
	path('<slug:game_slug>/door/open/<slug:room_slug>/', views.door_open, name='Open door'),
	path('<slug:game_slug>/door/close/<slug:room_slug>/', views.door_close, name='Close door'),

	# Challenge controls
	path('<slug:game_slug>/challenge/status/', views.challenge_status, name='Challenge Status'),
	path('<slug:game_slug>/challenge/solve/<slug:challenge_slug>/', views.challenge_solve, name='Solve Challenge'),
	path('<slug:game_slug>/challenge/reset/<slug:challenge_slug>/', views.challenge_reset, name='Reset Challenge'),
]
