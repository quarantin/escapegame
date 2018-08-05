# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [

	# Door controls
	path('door/<str:action>/<int:pin>/', views.set_door_locked),

	# Led controls
	path('led/<str:action>/<int:pin>/', views.set_led_state),

	# Challenge controls
	path('challenge/<str:action>/<int:pin>/', views.set_challenge_state),
]
