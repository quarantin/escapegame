# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from siteconfig import settings
from multimedia.models import MultimediaFile
from escapegame import libraspi

import os
import time
import traceback
import subprocess

from threading import Lock, Thread


MPV_ACTIONS = {
	'pause':        'cycle pause\n',
	'play':         'cycle pause\n',
	'stop':         'stop\n',
	'rewind':       'seek -10\n',
	'fast-forward': 'seek 10\n',
	'volume-down':  'cycle volume down\n',
	'volume-up':    'cycle volume up\n',
}

OMX_ACTIONS = {
	'pause':        'p',
	'play':         'p',
	'stop':         'q',
	'rewind':       '<',
	'fast-forward': '>',
	'volume-down':  '-',
	'volume-up':    '+',
}

class Command(BaseCommand):
	help = 'Video player background task'

	fifo_player = settings.VIDEO_PLAYER_FIFO
	fifo_control = settings.VIDEO_CONTROL_FIFO

	lock = Lock()

	pool = []
	zombies = []

	actions = settings.RUNNING_ON_PI and OMX_ACTIONS or MPV_ACTIONS

	process = None

	def wait_for_player_thread(self, media_file):

		self.process.wait()
		self.process = None

		media_file.status = 'stopped'
		media_file.save(update_fields=['status'])
		libraspi.notify_frontend()

		self.lock.acquire()
		self.zombies.append(self.pool.pop())
		self.lock.release()

	def control(self, action, media_id, url=None, loop=None):

		print('Video player: %s %s' % (action, url is not None and url or ''))

		if not action:
			return

		if action not in self.actions:
			raise Exception('Invalid player action: `%s`' % action)

		media_file = MultimediaFile.objects.get(pk=media_id)

		# If the video process has already been instanciated and is still running...
		if self.process is not None and self.process.poll() is None:

			# then we can communicate the command to the video process directly
			command = self.actions[action]

			if not os.path.exists(self.fifo_player):
				raise Exception('FATAL: Video player script is running but no player FIFO available!')

			fifo_player = open(self.fifo_player, 'w')
			fifo_player.write(command)
			fifo_player.close()

		# Otherwise, if the action is not 'stop' and we have a valid URL
		elif action is not 'stop' and url is not None:

			# Let's start the video player script
			script = os.path.join(settings.BASE_DIR, 'scripts/video-player.sh')
			argv = [ script, self.fifo_player, media_file.audio_out, url ]
			if loop is not None:
				argv.append('loop=true')

			self.process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=None, stderr=None)

			thread = Thread(target=self.wait_for_player_thread, args=(media_file,))

			self.lock.acquire()
			self.pool.append(thread)
			self.lock.release()

			thread.daemon = True
			thread.start()


		# Update status of multimedia file
		status = media_file.status

		if action == 'play':
			media_file.status = 'playing'

		elif action == 'pause':
			media_file.status = 'paused'

		elif action == 'stop':
			media_file.status = 'stopped'

		if status != media_file.status:
			media_file.save(update_fields=['status'])
			libraspi.notify_frontend()

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting video player background task'))

		delay = os.getenv('WAIT_DELAY') or 1

		while True:

			try:
				self.lock.acquire()
				for thread in self.zombies:
					thread.join()
				self.lock.release()

				if not os.path.exists(self.fifo_control):
					os.mkfifo(self.fifo_control)

				fifo_control = open(self.fifo_control, 'r')
				lines = fifo_control.read().strip().split('\n')
				fifo_control.close()

				for command in lines:
					cmd = command.strip().split(' ', 3)
					self.control(*cmd)

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
