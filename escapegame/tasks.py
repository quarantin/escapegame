# -*- coding: utf-8 -*-

from django.db import connection
from django.core.management import call_command

from background_task import background
from background_task.models import Task

from controllers.models import RaspberryPi

from .models import EscapeGame, EscapeGameChallenge

from . import libraspi

import time
import traceback


@background(schedule=0)
def cube_control(action, pin):
	call_command('clear-completed-tasks')
	return libraspi.cube_control(action, pin)

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

	print('Setting up background tasks!')

	try:
		controller = RaspberryPi.get_myself()

		games = EscapeGame.objects.all()
		for game in games:
			challs = game.get_challenges(controller=controller)
			for chall in challs:

				task_name = 'escapegame.tasks.poll_gpio'
				verbose_name = '%s.%s.%s.%s' % (task_name, game.slug, chall.room.slug, chall.slug)

				try:
					# If the task does not exist, this block will raise an exception.
					# Otherwise the background task is already installed, and we're good.
					task = Task.objects.get(task_name=task_name, verbose_name=verbose_name)
					continue

				except Task.DoesNotExist:

					# Instanciate the background task because we could not find it in database.
					poll_gpio(chall.id, task_name=task_name, verbose_name=verbose_name)

				except Exception as err:
					print('Error: %s' % traceback.format_exc())

	except Exception as err:
		print("Adding background tasks failed! (Error: %s)" % traceback.format_exc())

db_tables = connection.introspection.table_names()
if 'escapegame_escapegame' in db_tables:
	setup_background_tasks()
