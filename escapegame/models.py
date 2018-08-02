# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django_admin_conf_vars.global_vars import config

class VideoPlayer(models.Model):

	video_player = models.CharField(max_length=255)

	def __str__(self):
		return self.video_player

class Arduino(models.Model):

	name = models.CharField(max_length=255, default='')
	slug = models.SlugField(max_length=255, editable=False)
	ip_address = models.CharField(max_length=16)
	#wildcard/placeholder to replace in template (§IP_ADDRESS§)
	code_template = models.FileField(upload_to=config.UPLOAD_PATH)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(EscapeGame, self).save(*args, **kwargs)

class EscapeGame(models.Model):

	name = models.CharField(max_length=255, default='')
	slug = models.SlugField(max_length=255, editable=False)
	door_pin = models.IntegerField(default=3)
	door_pin_opened = models.BooleanField(default=False, editable=False)
	video_path = models.CharField(max_length=255)
	map_image_path = models.ImageField(upload_to=config.UPLOAD_PATH)
	sas_door_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')
	corridor_door_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(EscapeGame, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class EscapeGameRoom(models.Model):

	name = models.CharField(max_length=255, default='')
	slug = models.SlugField(max_length=255, editable=False)
	door_pin = models.IntegerField(default=5)
	door_pin_opened = models.BooleanField(default=False, editable=False)
	map_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')
	door_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')

	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(EscapeGameRoom, self).save(*args, **kwargs)

	def __str__(self):
		return '%s / %s' % (self.game, self.name)

class EscapeGameChallenge(models.Model):

	name = models.CharField(max_length=255, default='')
	slug = models.SlugField(max_length=255, editable=False)
	solved = models.BooleanField(default=False)
	challenge_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')

	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(EscapeGameChallenge, self).save(*args, **kwargs)

	def __str__(self):
		return '%s / %s' % (self.room, self.name)
