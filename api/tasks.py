from background_task import background
from escapegame.models import *

import socket

@background(schedule=0, repeat=0)
def poll_gpios():
	myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
	if not myself:
		return

	remote_pins = RemoteChallengePin.objects.filter(raspberrypi=myself)
	for remote_pin in remote_pins:
		poll_gpio.now(remote_pin.pin_number)

	
@background(schedule=60)
def poll_gpio(pin):
	open('/tmp/w00t-BBQ', 'w+').close()
	myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
	if not myself:
		print("ERROR: Could not find matching Raspberry Pi: %s.local" % socket.gethostname())
		return

	remote_pin = RemoteChallengePin.objects.filter(raspberrypi=myself, pin_number=pin)
	if not remote_pin:
		print("ERROR: Could not find matching remote challenge pin: %d on Raspberry Pi: %s.local" % (pin, socket.gethostname()))
		return

	callback_url_reset = remote_pin.callback_url_reset
	callback_url_validate = remote_pin.callback_url_validate

	print("Polling for GPIO pin %d in state %d" % (pin, state))
	while True:
		status, message = libraspi.wait_for_pin_state_change(pin, 5000)
		if message == 'Success':
			callback_url = (status == 0 and callback_url_reset or callback_url_validate)
			print("Performing request GET %s" % callback_url)
			libraspi.do_get(callback_url)
		
