# -*- coding: utf-8 -*-

from django.db import connection

from background_task import background
from background_task.models import Task

from multimedia.models import Video

from omxplayer import keys
from omxplayer.player import OMXPlayer
from omxplayer.bus_finder import BusFinder

import os
import time
import traceback


FIFO_PATH = '/tmp/player.fifo'
LOG_PATH = '/tmp/player.log'

@background(schedule=0)
def video_player_task(vid):

	method = 'multimedia.tasks.video_player_task'

	dbus_name = 'org.mpris.MediaPlayer2.omxplayer'

	video = Video.objects.all().first()

	logger = open(LOG_PATH, 'w')

	video_url = video.get_url()

	if os.path.exists(FIFO_PATH):
		os.remove(FIFO_PATH)

	old_url = None

	while True:

		try:

			if not os.path.exists(FIFO_PATH):
				logger.write('Creating fifo\n')
				logger.flush()
				os.mkfifo(FIFO_PATH)

				print('[ %s ] Starting video player task: %s' % (method, video_url))
				logger.write('Starting video player task: %s\n' % video_url)
				logger.flush()
				player = OMXPlayer(video_url, pause=True, dbus_name=dbus_name, args=[ '--no-osd', '--no-keys' ])

			fifo = open(FIFO_PATH, 'r')

			command = fifo.read().strip()

			fifo.close()

			if command == 'pause':
				logger.write('Running pause command\n')
				logger.flush()
				player.play_pause()

			elif command == 'stop':
				logger.write('Running stop command\n')
				logger.flush()
				player.stop()

			elif command in [ 'exit', 'quit', ]:
				logger.write('Running exit command\n')
				logger.flush()
				player.stop()
				break

			elif command.startswith('http'):
				logger.write('Running load URL command: %s\n' % command)
				logger.flush()
				if old_url is not None and old_url == command and player.playback_status() == 'Paused':
					player.play_pause()
				else:
					player.load(command)

				old_url = command

			else:
				logger.write('Ignoring unknown command: `%s`\n' % command)

			continue

		except Exception as err:
			print('[%s] Error: %s' % (method, traceback.format_exc()))

		try:
			# time.sleep() can raise some exceptions on some architectures,
			# so we call it from inside a try/except block just in case.
			time.sleep(1)

		except Exception as err:
			print('[%s] Error: %s' % (method, traceback.format_exc()))

		try:
			# If we arrive here, something went wrong, so let's try to cleanup the fifo
			if os.path.exists(FIFO_PATH):
				os.remove(FIFO_PATH)

		except Exception as err:
			print('[%s] Error: %s' % (method, traceback.format_exc()))

def setup_background_tasks():

	try:
		task_name = 'multimedia.tasks.video_player_task'
		verbose_name = task_name

		try:
			# If the task does not exist, this block will raise an exception.
			# Otherwise the background task is already installed, and we're good.
			task = Task.objects.get(task_name=task_name, verbose_name=verbose_name)
			return

		except Task.DoesNotExist:

			# Instanciate the background task because we could not find it in database.
			video_player_task(0, verbose_name=verbose_name)

		except Exception as err:
			print('Error: %s' % traceback.format_exc())

	except Exception as err:
		print("Adding background tasks failed! (Error: %s)" % traceback.format_exc())
