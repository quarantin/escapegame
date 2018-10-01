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

class PlayerControlMixin:

	fifo_path = None
	media_url = None

	def init(self, fifo_path, media_url):
		self.fifo_path = fifo_path
		self.media_url = media_url
		return self

	def fifo_control(self, command):
		try:
			if not os.path.exists(self.fifo_path):
				raise Exception('Player fifo does not exist! Please run: python3 manage.py video-player')

			fifo = open(self.fifo_path, 'w')
			fifo.write('%s\n' % command)
			fifo.close()

			return 0, 'Success'

		except:
			return 1, 'Error: %s' % traceback.format_exc()

	def pause(self):
		return self.fifo_control('pause')

	def play(self):
		return self.fifo_control('play %s' % self.media_url)

	def stop(self):
		return self.fifo_control('stop')

	def control(self, action):

		if action == 'pause':
			return self.pause()

		elif action == 'stop':
			return self.stop()

		elif action == 'play':
			return self.play()

		return 1, 'Invalid action `%s`' % action

class Video(PlayerControlMixin, models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	path = models.FileField(upload_to=settings.UPLOAD_VIDEO_PATH)

	def __init__(self, *args, **kwargs):
		super(Video, self).__init__(*args, **kwargs)

		# Initialize PlayerControlMixin
		self.init(settings.VIDEO_CONTROL_FIFO, self.get_url())

	def __str__(self):
		return 'Video - %s' % self.name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(Video, self).save(*args, **kwargs)

	def get_url(self, request=None, controller=None):
		from controllers.models import RaspberryPi
		from escapegame import libraspi
		controller = controller or RaspberryPi.get_master()
		host, port, protocol = libraspi.get_net_info(controller)
		return '%s://%s%s%s' % (protocol, host, port, self.path.url)

	class Meta:
		ordering = [ 'name' ]

class Audio(PlayerControlMixin, models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	path = models.FileField(upload_to=settings.UPLOAD_AUDIO_PATH)

	def __init__(self, *args, **kwargs):
		super(Audio, self).__init__(*args, **kwargs)

		# Initialize PlayerControlMixin
		self.init(settings.VIDEO_CONTROL_FIFO, self.get_url())

	def __str__(self):
		return 'Audio - %s' % self.name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(Audio, self).save(*args, **kwargs)

	def get_url(self, request=None, controller=None):
		from controllers.models import RaspberryPi
		from escapegame import libraspi
		controller = controller or RaspberryPi.get_master()
		host, port, protocol = libraspi.get_net_info(controller)
		return '%s://%s%s%s' % (protocol, host, port, self.path.url)

	class Meta:
		ordering = [ 'name' ]
