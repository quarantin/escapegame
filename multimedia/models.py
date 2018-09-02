# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify

from constance import config

from controllers.models import RaspberryPi

import os
import traceback


# Multimedia classes

class Image(models.Model):

	image_name = models.CharField(max_length=255, unique=True)
	image_path = models.ImageField(upload_to=config.UPLOAD_IMAGE_PATH)
	width = models.IntegerField()
	height = models.IntegerField()

	def __str__(self):
		return self.image_path.url

	def save(self, *args, **kwargs):
		self.width = self.image_path.width
		self.height = self.image_path.height
		super(Image, self).save(*args, **kwargs)

	def natural_key(self):
		return ( self.image_name, self.image_path.url, self.width, self.height )

class Video(models.Model):

	slug = models.SlugField(max_length=255, unique=True)
	video_name = models.CharField(max_length=255, unique=True)
	video_path = models.FileField(upload_to=config.UPLOAD_VIDEO_PATH)
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.video_path.url

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.video_name)
		self.clean()
		super(Video, self).save(*args, **kwargs)

	def __local_video_control_pause(fifo):

		if RUNNING_ON_PI:
			status, message = OMXPlayer().pause()

		else:
			status, message = 1, 'Fifo %s could not be found' % fifo
			if os.path.exists(fifo):
				fout = open(fifo, 'w')
				fout.write('pause\n')
				fout.close()
				status, message = 0, 'Success'

		return status, message

	def __local_video_control_play(fifo, video_path):

		if RUNNING_ON_PI:
			OMXPlayer(video_path)
			status = 0

		else:
			if os.path.exists(fifo):
				os.remove(fifo)

			os.mkfifo(fifo)

			status = subprocess.call([ config.VIDEO_PLAYER, '--input-file', fifo, video_path ])

			os.remove(fifo)

		return status, 'Success'

	def __local_video_control_stop():

		if RUNNING_ON_PI:
			status, message = OMXPlayer().stop()

		else:
			status, message = subprocess.call([ 'killall', config.VIDEO_PLAYER ]), 'Success'

		return status, message

	def control(action, video):

		try:
			if action not in [ 'pause', 'play', 'stop' ]:
				raise Exception('Invalid action `%s` in method video_control()' % action)

			fifo = '/tmp/%s.fifo' % video.slug

			host, port = get_master()

			video_url = 'http://%s%s/media%s' % (host, port, video.video_path.url)

			if action == 'pause':
				print("Pausing video '%s'" % video.video_name)
				return __local_video_control_pause(fifo)

			elif action == 'play':
				print("Playing video '%s'" % video.video_name)
				return __local_video_control_play(fifo, video_path)

			elif action == 'stop':
				print("Stopping video '%s'" % video.video_path.url)
				return __local_video_control_stop()

		except Exception as err:
			return 1, 'Error: %s' % traceback.format_exc()

if config.RUNNING_ON_PI:

	import dbus
	import getpass

	from omxplayer import keys, player
	from omxplayer.bus_finder import BusFinder

	DBUS_NAME = 'org.mpris.MediaPlayer2.omxplayer'

	class OMXPlayer:

		dbus_name = None
		controls = None
		properties = None

		def __init__(self, video_path=None, dbus_name=DBUS_NAME):

			# Store dbus name
			self.dbus_name = dbus_name

			# If a video was supplied, start playing it now
			if video_path:
				self.play(video_path)

			# Initialize DBUS controls and properties
			self.__init_controls()

		def __init_controls(self):

			try:
				socket_path = '/tmp/omxplayerdbus.%s' % getpass.getuser()
				if not os.path.exists(socket_path):
					socket_path = '/tmp/omxplayerdbus.root'
					if not os.path.exists(socket_path):
						return

				# Get the bus connection of omxplayer
				bus = dbus.bus.BusConnection(BusFinder().get_address())

				# Retrieve omxplayer dbus handle
				handle = bus.get_object(self.dbus_name, '/org/mpris/MediaPlayer2', introspect=False)

				# Retrieve omxplayer controls and properties through dbus handle
				self.controls = dbus.Interface(handle, 'org.mpris.MediaPlayer2.Player')
				self.properties = dbus.Interface(handle, 'org.freedesktop.DBus.Properties')

			except Exception as err:
				pass

		def __basic_control(self, key):

			try:
				if not self.controls:

					self.__init_controls()
					if not self.controls:
						return 1, 'No video running'

				self.controls.Action(key)
				return 0, 'Success'

			except Exception as err:
				print('Error: %s' % err)
				return 1, str(err)

		def __basic_property(self, key):

			try:
				if not self.properties:

					self.__init_controls()
					if not self.properties:
						return

				return self.properties.Get(key)

			except Exception as err:
				print('Error: %s' % err)

		def duration(self):
			return self.__basic_property('Duration')

		def fast_forward(self):
			return self.__basic_control(keys.FAST_FORWARD)

		def pause(self):
			return self.__basic_control(keys.PAUSE)

		def play(self, video):
			player.OMXPlayer(video, pause=False, dbus_name=self.dbus_name, args=[ '--no-osd' ])

		def position(self):
			return self.__basic_property('Position')

		def stop(self):
			return self.__basic_control(keys.EXIT)

		def rewind(self):
			return self.__basic_control(keys.REWIND)

