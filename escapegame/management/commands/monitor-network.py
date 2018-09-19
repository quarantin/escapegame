# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from controllers.models import RaspberryPi
from escapegame import libraspi

import os
import time
import traceback

from threading import Thread

class Command(BaseCommand):
	help = 'Monitor which Raspberry Pis are online'

	raspis = {}
	threads = {}

	def monitor_thread(self, raspi, delay):

		status = False

		while raspi in self.raspis:

			try:
				# Update online status of Raspberry Pi
				raspi.is_online()

			except KeyboardInterrupt:
				print('Quitting from thread! (because we received SIGINT)')
				break
			except:
				self.stdout.write(traceback.format_exc())

			try:
				time.sleep(delay)

			except KeyboardInterrupt:
				print('Quitting from thread! (because we received SIGINT)')
				break
			except:
				self.stdout.write(traceback.format_exc())

		print('Raspberry Pi %s is not registered anymore, quitting thread!' % raspi.hostname)

	def cleanup_threads(self):

		# For each of our threads
		for raspi in list(self.threads):

			thread = self.threads[raspi]

			# Check if it's alive
			if not thread.is_alive():

				# Join it if it's not
				thread.join()

				# And remove it from the thread list
				del self.threads[thread]

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting process to monitor Raspberry Pis'))

		delay = os.getenv('SLEEP_DELAY') or 5

		while True:

			try:
				# Retrieve all Raspberry Pis from database
				self.raspis = [ x for x in RaspberryPi.objects.all() ]

				# For each Raspberry Pi
				for raspi in self.raspis:

					# If we don't already have a thread for this Raspberry Pi
					if raspi not in self.threads:

						# Create new monitoring thread for this Raspberry Pi
						self.threads[raspi] = Thread(target=self.monitor_thread, args=(raspi, delay))
						self.threads[raspi].start()

						print('Starting new monitoring thread for Raspberry Pi `%s`' % raspi.hostname)

				# Cleanup dead threads
				self.cleanup_threads()

			except KeyboardInterrupt:
				print('Quitting! (because we received SIGINT)')
				break
			except:
				self.stdout.write(traceback.format_exc())

			try:
				time.sleep(delay)

			except KeyboardInterrupt:
				print('Quitting! (because we received SIGINT)')
				break
			except:
				self.stdout.write(traceback.format_exc())
