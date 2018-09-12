# -*- coding: utf-8 -*-

from siteconfig.celery import app

from controllers.models import ChallengeGPIO, CubeGPIO

from escapegame import libraspi

import time
import traceback


@app.task
def cube_control(cube_id, action, delay=0):

	cube = CubeGPIO.objects.get(pk=cube_id)

	try:
		signal = (action == 'raise')
		action = (signal and 'Raising' or 'Lowering')

		print('%s cube %s in %s seconds...' % (action, cube.slug))

		time.sleep(delay)

		print('%s cube %s now.' % (action, cube.slug))

		status, message = libraspi.set_pin(cube.lower_pin, signal)
		if status != 0:
			raise Exception('libraspi.set_pin(%d, %s) failed' % cube.raise_pin, signal)

	except:
		print('Error: %s' % traceback.format_exc())

@app.task
def poll_challenge_gpio(gpio_id):

	gpio = ChallengeGPIO.objects.get(pk=gpio_id)

	method = 'task.poll.gpio.%d.%s' % (gpio.action_pin, gpio.slug)

	print('[%s] Polling for GPIO %d' % (method, gpio.action_pin))

	while True:

		try:
			# First check current status of the GPIO so our database is consistant
			status, message, signal = libraspi.get_pin(gpio.action_pin)
			if status != 0:
				raise Exception('libraspi.get_pin() failed')

			# If this is not the state of the GPIO in database, then update it
			if signal != gpio.solved:
				gpio.solved = signal
				gpio.save()

			# Wait for a change on the GPIO
			status, message = libraspi.wait_for_pin_state_change(gpio.action_pin)
			if message != 'Success':
				raise Exception('libraspi.wait_for_pin_state_change() failed')

			# We just got a change on the GPIO, retrieve the value and update database
			status, message, signal = libraspi.get_pin(gpio.action_pin)
			if status != 0:
				raise Exception('libraspi.get_pin() failed')

			# If this is not the state of the GPIO in database, then update it
			if signal != gpio.solved:
				gpio.solved = signal
				gpio.save()

			continue

		except:
			print('[%s] Error: %s' % (method, traceback.format_exc()))

		# If we arrive here something went wrong, so let's just sleep a bit
		# before next iteration to avoid CPU overhead.
		try:
			# time.sleep() can raise some exceptions on some architectures,
			# so we call it from inside a try/except block just in case.
			time.sleep(1)

		except:
			print('[%s] Error: %s' % (method, traceback.format_exc()))
