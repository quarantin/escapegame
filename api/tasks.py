from background_task import background

from constance import config

from escapegame.models import *

import time


@background(schedule=0)
def poll_gpio(pin):

	myself = RaspberryPi.objects.get(hostname=config.HOSTNAME)
	if not myself:
		print("Could not find matching Raspberry Pi: %s" % config.HOSTNAME)
		return

	challenges = EscapeGameChallenge.objects.filter(challenge_pin=pin)
	remote_pin = RemoteChallengePin.objects.get(raspberrypi=myself, challenge__in=challenges)
	if not remote_pin:
		print("Could not find matching remote challenge pin: %d on Raspberry Pi: %s" % (pin, config.HOSTNAME))
		return

	url_callback_reset = remote_pin.url_callback_reset
	url_callback_validate = remote_pin.url_callback_validate

	print("Polling for GPIO pin %d" % pin)
	while True:

		try:
			status, message = libraspi.wait_for_pin_state_change(pin)
			if message != 'Success':
				raise Exception('libraspi.wait_for_pin_state_change() failed')

			status, message = libraspi.get_pin_state(pin)
			if message != 'Success':
				raise Exception('libraspi.get_pin_state() failed')

			callback_url = (status == 0 and url_callback_reset or url_callback_validate)

			print("Performing request GET %s" % callback_url)
			libraspi.do_get(callback_url)

		except Exception as err:
			print(err)

		time.sleep(1)
