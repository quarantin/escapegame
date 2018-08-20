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

	def __str__(self):
		return self.image_path.url

@json_import
class Video(models.Model):

	slug = models.SlugField(max_length=255)
	video_name = models.CharField(max_length=255)
	video_path = models.FileField(upload_to=config.UPLOAD_VIDEO_PATH)
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.video_path.path

	def save(self, *args, **kwargs):
		self.slug = slugify(self.video_name)
		super(Video, self).save(*args, **kwargs)

@json_import
class VideoPlayer(models.Model):

	video_player_name = models.CharField(max_length=255)
	video_player_path = models.CharField(max_length=255)

	def __str__(self):
		return self.video_player_path
