from django.contrib import admin
from escapegame.models import RaspberryPi, RemoteChallengePin
from background_task.models import Task
from . import tasks

from constance import config

from escapegame.apps import EscapegameConfig as AppConfig

import socket

logger = AppConfig.logger

try:
	myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
	if myself:
		remote_pins = RemoteChallengePin.objects.filter(raspberrypi=myself)
		for remote_pin in remote_pins:
			try:
				task = Task.objects.get(task_name='%s.tasks.poll.gpio.%d' % (AppConfig.name, remote_pin.pin_number))
				if task:
					logger.info("Not adding background task %s, already present in db" % task.task_name)
					continue

			except Exeption as err:
				logger.error('Error: %s' % err)

			tasks.poll_gpio(remote_pin.pin_number)

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
