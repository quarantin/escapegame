# -*- coding: utf-8 -*-

from django.urls import path

from . import views


urlpatterns = [

	# Challenge controls
	path('challenge/<slug:game_slug>/<slug:room_slug>/<slug:challenge_slug>/<str:action>/', views.rest_challenge_control),

	# Door controls
	path('door/<slug:game_slug>/<slug:room_slug>/<str:action>/', views.rest_door_control),

	# Video controls
	path('video/<slug:video_slug>/<str:action>/', views.rest_video_control),
]
