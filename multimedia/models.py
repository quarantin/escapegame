# -*- coding: utf-8 -*-

from django.db import models

from constance import config

from jsonexport.decorators import json_import

# Multimedia classes

@json_import
class Image(models.Model):

	image_name = models.CharField(max_length=255)
	image_path = models.ImageField(upload_to=config.UPLOAD_PATH)

	def __str__(self):
		return self.image_path.url

@json_import
class Video(models.Model):

	video_name = models.CharField(max_length=255)
	video_path = models.CharField(max_length=255)

	def __str__(self):
		return self.video_path

@json_import
class VideoPlayer(models.Model):

	video_player_name = models.CharField(max_length=255)
	video_player_path = models.CharField(max_length=255)

	def __str__(self):
		return self.video_player_path
