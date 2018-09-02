# -*- coding: utf-8 -*-

from background_task import background

from .models import EscapeGame, EscapeGameChallenge

from . import libraspi

import time
import traceback


@background(schedule=0)
def poll_gpio(challenge_id):

	method = 'api.tasks.poll_gpio'

	chall = EscapeGameChallenge.objects.get(pk=challenge_id)

	print('[%s] Polling for GPIO pin %d' % (method, chall.challenge_pin))

	while True:

		try:
			status, message = libraspi.wait_for_pin_state_change(chall.challenge_pin)
			if message != 'Success':
				raise Exception('libraspi.wait_for_pin_state_change() failed')

			status, message = libraspi.get_pin_state(chall.challenge_pin)
			if message != 'Success':
				raise Exception('libraspi.get_pin_state() failed')

			chall.solved = status
			chall.save()

		except Exception as err:
			print('[%s] Error: %s' % traceback.format_exc())

		try:
			# time.sleep() can raise some exceptions on some architectures,
			# so we call it from inside a try/except block just in case.
			time.sleep(1)

		except Exception as err:
			print('[%s] Error: %s' % traceback.format_exc())

def setup_background_tasks():

	try:
		controller = RaspberryPi.get_myself()

		games = EscapeGame.objects.all()
		for game in games:
			challs = game.get_challenges(controller=controller)
			for chall in challs:

				task_name = 'api.tasks.poll_gpio.%s.%s.%s' % (game.slug, chall.room.slug, chall.slug)
				verbose_name = '%s.%d' % (task_name, chall.id)

				try:
					task = Task.objects.get(task_name=task_name, verbose_name=verbose_name)
					if task:
						print("Not adding background task %s, already present in db" % task.verbose_name)
						continue

				except task.DoesNotExist:

					tasks.poll_gpio(challenge.id, verbose_name=verbose_name)

				except Exception as err:
					print('Error: %s' % traceback.format_exc())

	except Exception as err:
		print("Adding background tasks failed! (Error: %s)" % traceback.format_exc())

setup_background_tasks()
