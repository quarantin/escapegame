# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from controllers.models import RaspberryPi
from escapegame.models import EscapeGameChallenge

import os
import time
import requests
import traceback


class Command(BaseCommand):
	help = 'Listen for signal change on challenge GPIOs assigned to this controller.'

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting challenge GPIO polling process'))

		delay = os.getenv('WAIT_DELAY') or 1

		while True:

			try:
				# Retrieve the local Raspberry Pi
				myself = RaspberryPi.get_myself()
				if myself is None:
					raise Exception('I\'m not a registered controller, no GPIO to poll for (sleeping %d seconds).' % delay)

				# Retrieve all challenges
				challenges = EscapeGameChallenge.objects.all()

				# For each challenge assigned to this controller (myself),
				# check if the gpio is solved and notify the master if it is
				for chall in challenges:

					# We don't want to process challenges assigned to other controllers
					if chall.get_controller().id != myself.id:
						continue

					# If the challenge is not already solved in database, but the GPIO indicates it is solved...
					if chall.gpio.solved_at is None and chall.check_solved():

						# then notify the master about this challenge being solved, the master will update the database himself.
						print('Challenge solved on GPIO %d (%s)' % (chall.gpio.action_pin, chall.slug))
						requests.get(chall.callback_url_solve)

			except KeyboardInterrupt:
				print('Quitting! (Because we received SIGINT from user)')
				break
			except:
				self.stdout.write(traceback.format_exc())

			try:
				time.sleep(delay)

			except KeyboardInterrupt:
				print('Quitting! (Because we received SIGINT from user)')
				break
			except:
				self.stdout.write(traceback.format_exc())
