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

	# Challenge controls
	path('challenge/<str:action>/<int:pin>/', views.set_challenge_state),

	# Door controls
	path('door/<str:action>/<int:pin>/', views.set_door_locked),

	# Led controls
	path('led/<str:action>/<int:pin>/', views.set_led_state),
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
				task_name = '%s.tasks.poll.gpio.%d' % (AppConfig.name, remote_pin.pin_number)
				task = Task.objects.get(task_name=task_name)
				if task:
					logger.info("Not adding background task %s, already present in db" % task.task_name)
					continue

			except Exception as err:
				logger.error('Error: %s' % err)

			tasks.poll_gpio(remote_pin.pin_number, task_name=task_name)

except Exception as err:

	err = str(err)

	# SQLite3
	if err.startswith('no such table: escapegame_raspberrypi'):
		pass

	# MySQL
	if err.startswith('(1146, "Table \'escapegame.escapegame_raspberrypi\' doesn\'t exist")'):
		pass

	# No Raspberry Pi yet in database, or we are the master
	elif err.startswith('RaspberryPi matching query does not exist'):
		pass

	# We want to see other errors
	else:
		logger.error("Adding background tasks failed! (Error: %s)" % err)
