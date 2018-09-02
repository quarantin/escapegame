from background_task import background

from constance import config

from escapegame.models import EscapeGameChallenge
from controllers.models import RaspberryPi, RemoteChallengePin

import time


@background(schedule=0)
def poll_gpio(pin):

	method = 'api.tasks.poll_gpio(%d)' % pin

	myself = RaspberryPi.get_myself()
	if not myself:
		print('[%s] Could not find matching Raspberry Pi: %s' % (method, config.HOSTNAME))
		return

	challenges = EscapeGameChallenge.objects.filter(challenge_pin=pin)
	remote_pin = RemoteChallengePin.objects.get(raspberrypi=myself, challenge__in=challenges)
	if not remote_pin:
		print('[%s] Could not find matching remote challenge pin: %d on Raspberry Pi: %s' % (method, pin, config.HOSTNAME))
		return

	url_callback_reset = remote_pin.url_callback_reset
	url_callback_validate = remote_pin.url_callback_validate

	print('[%s] Polling for GPIO pin %d' % (method, pin))

	while True:

		try:
			status, message = libraspi.wait_for_pin_state_change(pin)
			if message != 'Success':
				raise Exception('libraspi.wait_for_pin_state_change() failed')

			status, message = libraspi.get_pin_state(pin)
			if message != 'Success':
				raise Exception('libraspi.get_pin_state() failed')

			callback_url = (status == 0 and url_callback_reset or url_callback_validate)

			print('[%s] Performing request GET %s' % (method, callback_url))
			libraspi.do_get(callback_url)

		except Exception as err:
			print('[%s] Error: %s' % err)

		try:
			# time.sleep() can raise some exceptions on some architectures,
			# so we call it from inside a try/except block just in case.
			time.sleep(1)

		except Exception as err:
			print('[%s] Error: %s' % err)
