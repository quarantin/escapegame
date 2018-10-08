# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from siteconfig import settings

import os
import traceback


# Multimedia classes

class Image(models.Model):

	name = models.CharField(max_length=255, unique=True)
	path = models.ImageField(upload_to=settings.UPLOAD_IMAGE_PATH)
	width = models.IntegerField()
	height = models.IntegerField()

	def __str__(self):
		return 'Image - %s' % self.name

	def save(self, *args, **kwargs):
		self.width = self.path.width
		self.height = self.path.height
		super(Image, self).save(*args, **kwargs)

	def natural_key(self):
		return ( self.name, self.path.url, self.width, self.height )

	class Meta:
		ordering = [ 'name' ]

class MultimediaFile(models.Model):

	TYPE_AUDIO = 'audio'
	TYPE_VIDEO = 'video'

	MEDIA_TYPES = (
		(TYPE_AUDIO, _('Audio')),
		(TYPE_VIDEO, _('Video')),
	)

	MEDIA_TYPES_DICT = {
		TYPE_AUDIO: _('Audio'),
		TYPE_VIDEO: _('Video'),
	}

	TYPE_AUDIO_OUT_BOTH = 'both'
	TYPE_AUDIO_OUT_HDMI = 'hdmi'
	TYPE_AUDIO_OUT_HEADPHONE = 'local'

	AUDIO_OUT_TYPES = (
		(TYPE_AUDIO_OUT_HDMI, _('HDMI')),
		(TYPE_AUDIO_OUT_HEADPHONE, _('Headphone')),
		(TYPE_AUDIO_OUT_BOTH, _('Both')),
	)

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	game = models.ForeignKey('escapegame.EscapeGame', on_delete=models.SET_NULL, blank=True, null=True)
	audio_out = models.CharField(max_length=6, default=TYPE_AUDIO_OUT_BOTH, choices=AUDIO_OUT_TYPES)
	media_type = models.CharField(max_length=6, default=TYPE_VIDEO, choices=MEDIA_TYPES)
	path = models.FileField(upload_to=settings.UPLOAD_MEDIA_PATH)
	status = models.CharField(max_length=255, default='stopped')

	def __str__(self):
		return '%s - %s' % (self.MEDIA_TYPES_DICT[self.media_type], self.name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(MultimediaFile, self).save(*args, **kwargs)

	def get_url(self, controller=None):
		from controllers.models import RaspberryPi
		from escapegame import libraspi
		controller = controller or RaspberryPi.get_master()
		host, port, protocol = libraspi.get_net_info(controller)
		return '%s://%s%s%s' % (protocol, host, port, self.path.url)

	def get_action_url(self, controller=None):
		from controllers.models import RaspberryPi
		from escapegame import libraspi
		controller = controller or RaspberryPi.get_master()
		host, port, protocol = libraspi.get_net_info(controller)
		return '%s://%s%s/en/api/video/%s/play/' % (protocol, host, port, self.slug)

	def fifo_control(self, command):
		try:
			fifo_path = settings.VIDEO_CONTROL_FIFO
			if not os.path.exists(fifo_path):
				raise Exception('Player fifo does not exist! Please run: python3 manage.py video-player')

			fifo = open(fifo_path, 'w')
			fifo.write('%s\n' % command)
			fifo.close()

			return 0, 'Success'

		except:
			return 1, 'Error: %s' % traceback.format_exc()

	def play(self):
		return self.fifo_control('play %s %s' % (self.pk, self.get_url()))

	def pause(self):
		return self.fifo_control('pause %s' % self.pk)

	def stop(self):
		return self.fifo_control('stop %s' % self.pk)

	def rewind(self):
		return self.fifo_control('rewind %s' % self.pk)

	def fast_forward(self):
		return self.fifo_control('fast-forward %s' % self.pk)

	def volume_down(self):
		return self.fifo_control('volume-down %s' % self.pk)

	def volume_up(self):
		return self.fifo_control('volume-up %s' % self.pk)

	def control(self, action):

		if action == 'play':
			return self.play()

		elif action == 'pause':
			return self.pause()

		elif action == 'stop':
			return self.stop()

		elif action == 'rewind':
			return self.rewind()

		elif action == 'fast-forward':
			return self.fast_forward()

		elif action == 'volume-down':
			return self.volume_down()

		elif action == 'volume-up':
			return self.volume_up()

		return 1, 'Invalid action `%s`' % action

	class Meta:
		ordering = [ 'name' ]
