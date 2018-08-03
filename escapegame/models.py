# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from constance import config

from escapegame import libraspi

import requests

class Video(models.Model):

	video_name = models.CharField(max_length=255)
	video_path = models.CharField(max_length=255)

	def __str__(self):
		return self.video_name

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

	image_type = models.CharField(max_length=255, choices=IMAGE_TYPE_CHOICES, default=TYPE_ROOM)
	image_path = models.ImageField(upload_to=config.UPLOAD_PATH)

	def __str__(self):
		return '%s / %s' % (self.image_type, self.image_path)

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

class RaspberryPi(models.Model):

	name = models.CharField(max_length=255)
	hostname = models.CharField(max_length=32)
	port = models.IntegerField(default=8000)
	validation_url = models.URLField(max_length=255)

	def __str__(self):
		return self.name

class EscapeGame(models.Model):

	escape_game_name = models.CharField(max_length=255, default='')
	escape_game_controller = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.CASCADE)
	video_brief = models.ForeignKey(Video, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=255, editable=False)

	sas_door_pin = models.IntegerField(default=7)
	corridor_door_pin = models.IntegerField(default=9)

	sas_door_locked = models.BooleanField(default=True)
	corridor_door_locked = models.BooleanField(default=True)

	map_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='game_map_image_path', limit_choices_to={ 'image_type': Image.TYPE_MAP })
	sas_door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='sas_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })
	corridor_door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='corridor_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })

	def set_sas_door_locked(self, locked):
		try:
			status, message = libraspi.set_door_locked(self.sas_door_pin, locked)
			if status == 0:
				self.sas_door_locked = locked
				self.save()

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

	def set_corridor_door_locked(self, locked):
		try:
			status, message = libraspi.set_door_locked(self.corridor_door_pin, locked)
			if status == 0:
				self.corridor_door_locked = locked
				self.save()

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

	def save(self, *args, **kwargs):
		self.slug = slugify(self.escape_game_name)
		super(EscapeGame, self).save(*args, **kwargs)

	def __str__(self):
		return self.escape_game_name

class EscapeGameRoom(models.Model):

	room_name = models.CharField(max_length=255, default='')
	room_controller = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.CASCADE)
	escape_game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=255, editable=False)

	door_pin = models.IntegerField(default=5)
	door_locked = models.BooleanField(default=True)

	room_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_image_path', limit_choices_to={ 'image_type': Image.TYPE_ROOM })
	door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })

	def set_door_locked(self, locked):
		try:
			print('set_door_lock(%s) [%s]' % (locked, self))
			status, message = libraspi.set_door_locked(self.door_pin, locked)
			if status == 0:
				self.door_locked = locked
				self.save()

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

	def set_remote_door_locked(self, host, port, action):
		try:
			print('set_remote_door_lock(%s, %d, %s) [%s]' % (host, port, action, self))
			locked = (action == 'lock')
			response = requests.get('http://%s:%d/api/door/%s/%d' % (host, port, action, self.door_pin))
			print("WTF")
			print(response.json())
			# TODO check response is valid
			# if response is valid:
			if True:
				self.door_locked = locked
				self.save()

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error %s' % err

	def save(self, *args, **kwargs):
		self.slug = slugify(self.room_name)
		super(EscapeGameRoom, self).save(*args, **kwargs)

	def __str__(self):
		return '%s / %s' % (self.escape_game, self.room_name)

class EscapeGameChallenge(models.Model):

	challenge_name = models.CharField(max_length=255, default='')
	slug = models.SlugField(max_length=255, editable=False)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	solved = models.BooleanField(default=False)
	challenge_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='chall_map_image_path', limit_choices_to={ 'image_type': Image.TYPE_CHALL })

	def set_solved(self, solved):
		try:
			self.solved = solved
			self.save()
			return 0, 'Success'

		except Exeption as err:
			return 1, 'Error: %s' % err

	def save(self, *args, **kwargs):
		self.slug = slugify(self.challenge_name)
		super(EscapeGameChallenge, self).save(*args, **kwargs)

	def __str__(self):
		return '%s / %s' % (self.room, self.challenge_name)
