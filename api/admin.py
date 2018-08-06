from django.contrib import admin
from escapegame.models import RaspberryPi, RemoteChallengePin
from . import tasks

from constance import config

import socket

try:
	myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
	if myself:
		remote_pins = RemoteChallengePin.objects.filter(raspberrypi=myself)
		for remote_pin in remote_pins:
			tasks.poll_gpio(remote_pin.pin_number)

except Exception as err:

	err = str(err)

	if err.startswith('no such table: escapegame_raspberrypi'):
		pass

	elif err.startswith('RaspberryPi matching query does not exist') and config.IS_MASTER:
		pass

	else:
		print("Adding background tasks failed! (Error: %s)" % err)
