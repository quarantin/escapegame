# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from controllers.models import ChallengeGPIO, RaspberryPi

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
				# Retrive the local Raspberry Pi
				myself = RaspberryPi.get_myself()
				if myself is None:
					raise Exception('I\'m not a registered controller, no GPIO to poll for.')

				# Retrieve all GPIOs from this controller
				gpios = ChallengeGPIO.objects.filter(controller=myself)

				# For each GPIO check if the challenge is solved and notify the master if it is
				for gpio in gpios:

					# If the challenge is not already solved in database, but the GPIO indicates it is solved...
					if not gpio.solved and gpio.check_solved():

						# then notify the master about this challenge being solved
						print('Challenge solved on GPIO %d (%s)' % (gpio.action_pin, gpio.challenge.slug))
						requests.get(gpio.challenge.callback_url_solve)

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
