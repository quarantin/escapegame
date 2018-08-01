# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [

	# Escape game selector view
	path('', views.index, name='Index'),

	# Escape game control view
	path('<slug:slug>', views.escapegame, name='Escape Game'),
	path('<slug:slug>/start', views.escapegame_start, name='Start Escape Game'),

	# Video controls
	path('<slug:slug>/video/play', views.video_play, name='Play Brief Video'),
	path('<slug:slug>/video/stop', views.video_stop, name='Stop Brief Video'),

	# Door controls
	path('<slug:slug>/door/<int:pin>', views.door_status, name='Door Status'),
	path('<slug:slug>/door/<int:pin>/open', views.door_open, name='Open door'),
	path('<slug:slug>/door/<int:pin>/close', views.door_close, name='Close door'),

	# Challenge controls
	path('<slug:slug>/challenge/status', views.challenge_status, name='Challenge Status'),
	path('<slug:slug>/challenge/<int:challenge>/solve', views.challenge_solve, name='Solve Challenge'),
	path('<slug:slug>/challenge/<int:challenge>/reset', views.challenge_reset, name='Reset Challenge'),
]
