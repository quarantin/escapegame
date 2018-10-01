# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify

from siteconfig import settings

import os
import traceback


# Multimedia classes

class Image(models.Model):

	image_name = models.CharField(max_length=255, unique=True)
	image_path = models.ImageField(upload_to=settings.UPLOAD_IMAGE_PATH)
	width = models.IntegerField()
	height = models.IntegerField()

	def __str__(self):
		return 'Image - %s' % self.image_name

	def save(self, *args, **kwargs):
		self.width = self.image_path.width
		self.height = self.image_path.height
		super(Image, self).save(*args, **kwargs)

	def natural_key(self):
		return ( self.image_name, self.image_path.url, self.width, self.height )

	class Meta:
		ordering = [ 'image_name' ]

class Video(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	video_name = models.CharField(max_length=255, unique=True)
	video_path = models.FileField(upload_to=settings.UPLOAD_VIDEO_PATH)

	def __str__(self):
		return 'Video - %s' % self.video_name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.video_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(Video, self).save(*args, **kwargs)

	def send_command(self, command):
		try:
			from siteconfig import settings
			fifo_path = settings.VIDEO_CONTROL_FIFO
			if not os.path.exists(fifo_path):
				raise Exception('Player fifo does not exist!')

			fifo = open(fifo_path, 'w')
			fifo.write(command)
			fifo.close()

			return 0, 'Success'

		except:
			return 1, 'Error: %s' % traceback.format_exc(),

	def get_url(self, request=None, controller=None):
		from controllers.models import RaspberryPi
		from escapegame import libraspi
		controller = controller or RaspberryPi.get_master()
		host, port, protocol = libraspi.get_net_info(controller)
		return '%s://%s%s%s' % (protocol, host, port, self.video_path.url)

	def control(self, action):

		if action == 'pause':
			return self.pause()

		elif action == 'stop':
			return self.stop()

		elif action == 'play':
			return self.play()

		return 1, 'Invalid action `%s`' % action

	def pause(self):
		return self.send_command('pause')

	def play(self):
		return self.send_command('play %s' % self.get_url())

	def stop(self):
		return self.send_command('stop')

	class Meta:
		ordering = [ 'video_name' ]

class Audio(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	audio_name = models.CharField(max_length=255, unique=True)
	audio_path = models.FileField(upload_to=settings.UPLOAD_AUDIO_PATH)

	def __str__(self):
		return 'Audio - %s' % self.audio_name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.audio_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(Audio, self).save(*args, **kwargs)

	def send_command(self, command):
		try:
			from siteconfig import settings
			fifo_path = settings.VIDEO_CONTROL_FIFO
			if not os.path.exists(fifo_path):
				raise Exception('Player fifo does not exist!')

			fifo = open(fifo_path, 'w')
			fifo.write(command)
			fifo.close()

			return 0, 'Success'

		except:
			return 1, 'Error: %s' % traceback.format_exc(),

	def get_url(self, request=None, controller=None):
		from controllers.models import RaspberryPi
		from escapegame import libraspi
		controller = controller or RaspberryPi.get_master()
		host, port, protocol = libraspi.get_net_info(controller)
		return '%s://%s%s%s' % (protocol, host, port, self.audio_path.url)

	def control(self, action):

		if action == 'pause':
			return self.pause()

		elif action == 'stop':
			return self.stop()

		elif action == 'play':
			return self.play()

		return 1, 'Invalid action `%s`' % action

	def pause(self):
		return self.send_command('pause')

	def play(self):
		return self.send_command('play %s' % self.get_url())

	def stop(self):
		return self.send_command('stop')

	class Meta:
		ordering = [ 'audio_name' ]
