# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify

from constance import config

from controllers.models import RaspberryPi
from jsonexport.decorators import json_import


# Multimedia classes

@json_import
class Image(models.Model):

	image_name = models.CharField(max_length=255)
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

@json_import
class Video(models.Model):

	slug = models.SlugField(max_length=255)
	video_name = models.CharField(max_length=255, default='')
	video_path = models.FileField(upload_to=config.UPLOAD_VIDEO_PATH)
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.video_path.url

	def save(self, *args, **kwargs):
		self.slug = slugify(self.video_name)
		super(Video, self).save(*args, **kwargs)

@json_import
class VideoPlayer(models.Model):

	video_player_name = models.CharField(max_length=255)
	video_player_path = models.CharField(max_length=255)

	def __str__(self):
		return self.video_player_path
