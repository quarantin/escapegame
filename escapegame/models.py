# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from constance import config

from escapegame import libraspi

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
	video_path = models.CharField(max_length=255)
	map_image_path = models.ImageField(upload_to=config.UPLOAD_PATH)

	sas_door_pin = models.IntegerField(default=7)
	sas_door_locked = models.BooleanField(default=True, editable=False)
	sas_door_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')

	corridor_door_pin = models.IntegerField(default=9)
	corridor_door_locked = models.BooleanField(default=True, editable=False)
	corridor_door_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')

	def set_sas_door_lock(self, locked):

		status, message = libraspi.set_door_lock(self.sas_door_pin, locked)
		if status == 0:
			self.sas_door_locked = locked
			self.save()

		return status, message

	def set_corridor_door_lock(self, locked):

		status, message = libraspi.set_door_lock(self.corridor_door_pin, locked)
		if status == 0:
			self.corridor_door_locked = locked
			self.save()

		return status, message

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(EscapeGame, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class EscapeGameRoom(models.Model):

	name = models.CharField(max_length=255, default='')
	slug = models.SlugField(max_length=255, editable=False)
	map_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')

	door_pin = models.IntegerField(default=5)
	door_locked = models.BooleanField(default=True, editable=False)
	door_image_path = models.ImageField(upload_to=config.UPLOAD_PATH, default='')

	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)

	def set_door_lock(self, locked):

		status, message = libraspi.set_door_lock(self.door_pin, locked)
		if status == 0:
			self.door_locked = locked
			self.save()

		return status, message

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
