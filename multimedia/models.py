# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify

from constance import config

from controllers.models import RaspberryPi

from escapegame import libraspi

from .player import VideoPlayer

import os
import traceback
import subprocess


# Multimedia classes

class Image(models.Model):

	image_name = models.CharField(max_length=255, unique=True)
	image_path = models.ImageField(upload_to=config.UPLOAD_IMAGE_PATH)
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
	video_path = models.FileField(upload_to=config.UPLOAD_VIDEO_PATH)

	def __str__(self):
		return 'Video - %s' % self.video_name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.video_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(Video, self).save(*args, **kwargs)

	def get_url(self, request):
		host, port, protocol = libraspi.get_net_info(request, RaspberryPi.get_master())
		return '%s://%s%s%s' % (protocol, host, port, self.video_path.url)

	def control(self, request, action):
		video_url = self.get_url(request)
		return VideoPlayer(video_url).control(request, action)

	class Meta:
		ordering = [ 'video_name' ]
