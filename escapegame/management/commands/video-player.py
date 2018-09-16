# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from multimedia.models import Video

import os
import time
import traceback


class Command(BaseCommand):
	help = 'Video player background task'

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting video player background task'))

		delay = os.getenv('WAIT_DELAY') or 1

		while True:

			try:
				raise Exception('Implement me!')

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
