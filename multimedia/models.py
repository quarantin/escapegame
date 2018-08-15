# -*- coding: utf-8 -*-

from django.db import models

from constance import config

from jsonexport.decorators import json_import

# Multimedia classes

@json_import
class Image(models.Model):

	TYPE_CHALL = 'challenge'
	TYPE_DOOR  = 'door'
	TYPE_MAP   = 'map'
	TYPE_ROOM  = 'room'

	IMAGE_TYPE_CHOICES = (
		(TYPE_CHALL, 'Challenge'),
		(TYPE_DOOR,  'Door'),
		(TYPE_MAP,   'Map'),
		(TYPE_ROOM,  'Room'),
	)

	image_name = models.CharField(max_length=255)
	image_type = models.CharField(max_length=255, choices=IMAGE_TYPE_CHOICES, default=TYPE_ROOM)
	image_path = models.ImageField(upload_to=config.UPLOAD_PATH)

	def __str__(self):
		return '%s [%s] (%s)' % (self.image_name, self.image_type, self.image_path)

@json_import
class Video(models.Model):

	video_name = models.CharField(max_length=255)
	video_path = models.CharField(max_length=255)

	def __str__(self):
		return '%s (%s)' % (self.video_name, self.video_path)

@json_import
class VideoPlayer(models.Model):

	video_player_name = models.CharField(max_length=255)
	video_player_path = models.CharField(max_length=255)

	def __str__(self):
		return '%s (%s)' % (self.video_player_name, self.video_player_path)
