# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from import_export import resources
from constance import config

from escapegame.apps import EscapegameConfig as AppConfig
logger = AppConfig.logger

from escapegame import libraspi

import os
import socket
import requests

# Media classes

"""
Class to represent an image. Images are used to represent visual objects on a map,
like doors, challenges, rooms, or even a whole escape game map.
"""
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

"""
Class to represent a video. Video are played at the begining of escape game,
when the challengers enter the SAS.
"""
class Video(models.Model):

	video_name = models.CharField(max_length=255)
	video_path = models.CharField(max_length=255)

	def __str__(self):
		return self.video_name

class VideoPlayer(models.Model):

	video_player = models.CharField(max_length=255)

	def __str__(self):
		return self.video_player


# Escape game classes

class EscapeGame(models.Model):

	escape_game_name = models.CharField(max_length=255, default='')
	escape_game_controller = models.ForeignKey('RaspberryPi', blank=True, null=True, on_delete=models.CASCADE)
	video_brief = models.ForeignKey(Video, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=255)

	sas_door_pin = models.IntegerField(default=7)
	corridor_door_pin = models.IntegerField(default=10)

	sas_door_locked = models.BooleanField(default=True)
	corridor_door_locked = models.BooleanField(default=True)

	map_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='game_map_image_path', limit_choices_to={ 'image_type': Image.TYPE_MAP })
	sas_door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='sas_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })
	corridor_door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='corridor_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })

	def set_door_locked(self, door, locked):
		try:
			if door == 'sas':
				door_pin = self.sas_door_pin

			elif door == 'corridor':
				door_pin = self.corridor_door_pin

			else:
				raise Exception('Invalid door \'%s\'' % door)

			status, message = libraspi.set_door_locked(door_pin, locked)
			if status == 0:
				self.sas_door_locked = locked
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
	room_controller = models.ForeignKey('RaspberryPi', blank=True, null=True, on_delete=models.CASCADE)
	escape_game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=255)

	door_pin = models.IntegerField(default=5)
	door_locked = models.BooleanField(default=True)

	room_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_image_path', limit_choices_to={ 'image_type': Image.TYPE_ROOM })
	door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })

	def set_door_locked(self, locked):
		try:
			logger.info('set_door_lock(%s) [%s]' % (locked, self))
			status, message = libraspi.set_door_locked(self.door_pin, locked)
			if status == 0:
				self.door_locked = locked
				self.save()

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

	def save(self, *args, **kwargs):
		self.slug = slugify(self.room_name)
		super(EscapeGameRoom, self).save(*args, **kwargs)

	def __str__(self):
		return '%s / %s' % (self.escape_game, self.room_name)

class EscapeGameChallenge(models.Model):

	challenge_name = models.CharField(max_length=255, default='')
	slug = models.SlugField(max_length=255)
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


# Remote pin classes

class RaspberryPi(models.Model):

	name = models.CharField(max_length=255)
	hostname = models.CharField(max_length=32)
	port = models.IntegerField(default=8000)

	def __str__(self):
		return self.name

class RemoteChallengePin(models.Model):
	
	name = models.CharField(max_length=255)
	challenge = models.ForeignKey(EscapeGameChallenge, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	pin_number = models.IntegerField(default=7)
	callback_url_validate = models.URLField(max_length=255)
	callback_url_reset = models.URLField(max_length=255)

	def save(self, *args, **kwargs):

		host = config.MASTER_HOSTNAME
		port = (config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or '')
		game_slug = self.challenge.room.escape_game.slug
		room_slug = self.challenge.room.slug
		chall_slug = self.challenge.slug

		self.callback_url_validate = 'http://%s%s/web/%s/%s/%s/validate/' % (host, port, game_slug, room_slug, chall_slug)
		self.callback_url_reset = 'http://%s%s/web/%s/%s/%s/reset/' % (host, port, game_slug, room_slug, chall_slug)

		super(RemoteChallengePin, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class RemoteDoorPin(models.Model):

	name = models.CharField(max_length=255)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	pin_number = models.IntegerField(default=7)
	callback_url_lock = models.URLField(max_length=255)
	callback_url_unlock = models.URLField(max_length=255)

	def save(self, *args, **kwargs):

		host = config.MASTER_HOSTNAME
		port = (config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or '')
		game_slug = self.room.escape_game.slug
		room_slug = self.room.slug

		self.callback_url_lock = 'http://%s%s/web/%s/%s/lock/' % (host, port, game_slug, room_slug)
		self.callback_url_unlock = 'http://%s%s/web/%s/%s/unlock/' % (host, port, game_slug, room_slug)

		super(RemoteDoorPin, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class RemoteLedPin(models.Model):

	name = models.CharField(max_length=255)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	pin_number = models.IntegerField(default=7)
	url_on = models.URLField(max_length=255)
	url_off = models.URLField(max_length=255)

	def save(self, *args, **kwargs):

		host = self.raspberrypi.hostname
		port = (self.raspberrypi.port != 80 and ':%d' % self.raspberrypi.port or '')

		self.url_on = 'http://%s%s/api/led/on/%d/' % (host, port, self.pin_number)
		self.url_off = 'http://%s%s/api/led/off/%d/' % (host, port, self.pin_number)

		super(RemoteLedPin, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

