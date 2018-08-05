from django.contrib import admin
from escapegame.models import RaspberryPi, RemoteChallengePin
from . import tasks

import socket

try:
	myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
	if myself:
		remote_pins = RemoteChallengePin.objects.filter(raspberrypi=myself)
		for remote_pin in remote_pins:
			poll_gpio.now(remote_pin.pin_number)

except Exception as err:
	print("Adding background tasks failed! (Error: %s)" % err)
