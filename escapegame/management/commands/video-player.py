# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from siteconfig import settings
from multimedia.models import Video

import os
import time
import traceback
import subprocess


MPV_ACTIONS = {
	'pause': 'cycle pause\n',
	'play':  'cycle pause\n',
	'stop':  'stop\n',
}

OMX_ACTIONS = {
	'pause': 'pause\n',
	'play':  'pause\n',
	'stop':  'stop\n',
}

class Command(BaseCommand):
	help = 'Video player background task'

	fifo = '/tmp/video-control.fifo'
	fifo_player = '/tmp/video-player.fifo'
	actions = settings.RUNNING_ON_PI and OMX_ACTIONS or MPV_ACTIONS

	process = None

	def control(self, action, url=None):

		print('Video player: %s %s' % (action, url is not None and url or ''))

		if action not in self.actions:
			raise Exception('Invalid player action: `%s`' % action)

		# If we don't have a valid URL, and if the video process has already been instanciated and is still running...
		if url is None and self.process is not None and self.process.poll() is None:

			# then we can communicate the command to the video process directly
			command = self.actions[action]

			if not os.path.exists(self.fifo_player):
				raise Exception('FATAL: Video player script is running but no player FIFO available!')

			fifo_player = open(self.fifo_player, 'w')
			fifo_player.write(command)
			fifo_player.close()

		# Otherwise, if the action was not 'stop' and we have a valid URL
		elif action is not 'stop' and url is not None:

			# Let's start the video player script
			script = os.path.join(settings.BASE_DIR, 'scripts/video-player.sh')
			self.process = subprocess.Popen([ script, self.fifo_player, url ], stdin=subprocess.PIPE, stdout=None, stderr=None)

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting video player background task'))

		delay = os.getenv('WAIT_DELAY') or 1

		while True:

			try:
				if not os.path.exists(self.fifo):
					os.mkfifo(self.fifo)

				fifo = open(self.fifo, 'r')
				command = fifo.read().strip().split(' ', 1)
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
