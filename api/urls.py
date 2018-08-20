# -*- coding: utf-8 -*-

from django.urls import path

from background_task.models import Task
from escapegame.apps import EscapegameConfig as AppConfig
from escapegame.models import RaspberryPi, RemoteChallengePin

from . import tasks
from . import views

import socket

logger = AppConfig.logger

urlpatterns = [

	# REST Token Authentication
	path('get-token/', views.get_token),

	# Challenge controls
	path('challenge/<str:action>/<int:pin>/', views.set_challenge_state),

	# Door controls
	path('door/<str:action>/<int:pin>/', views.set_door_locked),

	# Led controls
	path('led/<str:action>/<int:pin>/', views.set_led_state),

	# Video controls
	path('video/<slug:video_slug>/<str:action>/', views.set_video_state),
]

"""
	Install background tasks if needed.
"""

try:
	myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
	if myself:
		remote_pins = RemoteChallengePin.objects.filter(raspberrypi=myself)
		for remote_pin in remote_pins:
			try:
				challenge = remote_pin.challenge
				task_name = 'api.tasks.poll_gpio'
				verbose_name = '%s.tasks.poll.gpio.%d' % (AppConfig.name, challenge.challenge_pin)
				task = Task.objects.get(task_name=task_name, verbose_name=verbose_name)
				if task:
					print("Not adding background task %s, already present in db" % task.task_name)
					continue

			except Exception as err:
				print('Error: %s' % err)

			tasks.poll_gpio(challenge.challenge_pin, verbose_name=verbose_name)

except Exception as err:

	err = str(err)

	# SQLite3
	if err.startswith('no such table: escapegame_raspberrypi'):
		pass

	# MySQL
	if err.startswith('(1146, "Table \'escapegame.controllers_raspberrypi\' doesn\'t exist")'):
		pass

	# No Raspberry Pi yet in database, or we are the master
	elif err.startswith('RaspberryPi matching query does not exist'):
		pass

	# We want to see other errors
	else:
		print("Adding background tasks failed! (Error: %s)" % err)
