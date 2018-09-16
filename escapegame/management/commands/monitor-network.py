# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from controllers.models import RaspberryPi
from escapegame import libraspi

import os
import time
import traceback


class Command(BaseCommand):
	help = 'Monitor which Raspberry Pis are online'

	def reset_online_status(self):
		raspis = RaspberryPi.objects.all()
		for raspi in raspis:
			raspi.online = False
			raspi.save()

		libraspi.notify_frontend()

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting process to monitor Raspberry Pis'))

		self.reset_online_status()

		delay = os.getenv('SLEEP_DELAY') or 5

		status = {}

		while True:

			try:
				raspis = RaspberryPi.objects.all()

				for raspi in raspis:

					if raspi.hostname not in status:
						status[raspi.hostname] = False

					online = raspi.is_online()
					if online != status[raspi.hostname]:
						status[raspi.hostname] = online
						libraspi.notify_frontend()
						print(status)

			except KeyboardInterrupt:
				print('Quitting! (because we received SIGINT)')
				break
			except:
				self.stdout.write(traceback.format_exc())

			try:
				print('About to sleep %d seconds' % delay)
				time.sleep(delay)

			except KeyboardInterrupt:
				print('Quitting! (because we received SIGINT)')
				break
			except:
				self.stdout.write(traceback.format_exc())
