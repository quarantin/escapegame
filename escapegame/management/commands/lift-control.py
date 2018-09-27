# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from siteconfig import settings
from controllers.models import LiftGPIO
from escapegame import libraspi

import os
import time
import traceback
import subprocess

from threading import Thread


class Command(BaseCommand):
	help = 'Lift control background task'

	fifo = settings.LIFT_CONTROL_FIFO
	actions = [ 'lower', 'raise' ]

	processes = {}

	def delayed_control(self, pin, signal, delay):

		signal_str = signal and 'HIGH' or 'LOW'
		print('Lift control: delayed_control(pin=%s, signal=%s, delay=%s)' % (pin, signal_str, delay))

		time.sleep(int(delay))

		libraspi.set_pin(pin, signal)

	def control(self, action, lift_slug, delay):

		if action not in self.actions:
			raise Exception('Invalid action `%s`' % action)

		signal = (action == 'raise')

		lift = LiftGPIO.objects.get(slug=lift_slug)

		Thread(target=self.delayed_control, args=(lift.pin, signal, delay)).start()

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting lift control background task'))

		delay = os.getenv('WAIT_DELAY') or 1

		while True:

			try:
				if not os.path.exists(self.fifo):
					os.mkfifo(self.fifo)

				fifo = open(self.fifo, 'r')
				command = fifo.read().strip().split(' ', 2)
				fifo.close()

				self.control(*command)
				continue

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
