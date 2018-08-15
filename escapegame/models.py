# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from constance import config

from multimedia.models import Image, Video

from jsonexport.util import generic_json_import, generic_json_import_list

from escapegame.apps import EscapegameConfig as AppConfig
logger = AppConfig.logger

from escapegame import libraspi

import os
import socket
import requests
import traceback


# Escape game classes

class EscapeGame(models.Model):

	slug = models.SlugField(max_length=255)
	escapegame_name = models.CharField(max_length=255, default='')
	raspberrypi = models.ForeignKey('RaspberryPi', blank=True, null=True, on_delete=models.CASCADE)
	video_brief = models.ForeignKey(Video, on_delete=models.CASCADE)

	sas_door_pin = models.IntegerField(default=7)
	corridor_door_pin = models.IntegerField(default=10)

	sas_door_locked = models.BooleanField(default=True)
	corridor_door_locked = models.BooleanField(default=True)

	map_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='game_map_image_path', limit_choices_to={ 'image_type': Image.TYPE_MAP })
	sas_door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='sas_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })
	corridor_door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='corridor_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })

	def __str__(self):
		return self.escapegame_name

	def json_import(jsondata):
		return generic_json_import(EscapeGame, jsondata)

	def json_import_list(jsondata):
		return generic_json_import_list(EscapeGame, jsondata)

	def save(self, **kwargs):
		self.slug = slugify(self.escapegame_name)
		super(EscapeGame, self).save(**kwargs)

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

class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255)
	room_name = models.CharField(max_length=255, default='')
	escapegame = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey('RaspberryPi', blank=True, null=True, on_delete=models.CASCADE)

	door_pin = models.IntegerField(default=5)
	door_locked = models.BooleanField(default=True)

	room_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_image_path', limit_choices_to={ 'image_type': Image.TYPE_ROOM })
	door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })

	def __str__(self):
		return '%s / %s' % (self.escapegame, self.room_name)

	def json_import(jsondata):
		return generic_json_import(EscapeGameRoom, jsondata)

	def json_import_list(jsondata):
		return generic_json_import_list(EscapeGameRoom, jsondata)

	def save(self, **kwargs):
		self.slug = slugify(self.room_name)
		super(EscapeGameRoom, self).save(**kwargs)

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

class EscapeGameChallenge(models.Model):

	slug = models.SlugField(max_length=255)
	challenge_name = models.CharField(max_length=255, default='')
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	challenge_pin = models.IntegerField(default=31)
	solved = models.BooleanField(default=False)

	challenge_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='chall_map_image_path', limit_choices_to={ 'image_type': Image.TYPE_CHALL })

	def __str__(self):
		return '%s / %s' % (self.room, self.challenge_name)

	def json_import(jsondata):
		return generic_json_import(EscapeGameChallenge, jsondata)

	def json_import_list(jsondata):
		return generic_json_import_list(EscapeGameChallenge, jsondata)

	def save(self, **kwargs):
		self.slug = slugify(self.challenge_name)
		super(EscapeGameChallenge, self).save(**kwargs)

	def set_solved(self, solved):
		try:
			self.solved = solved
			self.save()
			return 0, 'Success'

		except Exeption as err:
			return 1, 'Error: %s' % err


# Remote pin classes

class RaspberryPi(models.Model):

	name = models.CharField(max_length=255)
	hostname = models.CharField(max_length=32)
	port = models.IntegerField(default=8000)

	def __str__(self):
		return self.name

	def json_import(jsondata):
		return generic_json_import(RaspberryPi, jsondata)

	def json_import_list(jsondata):
		return generic_json_import_list(RaspberryPi, jsondata)

class RemoteChallengePin(models.Model):
	
	name = models.CharField(max_length=255)
	challenge = models.ForeignKey(EscapeGameChallenge, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	url_callback_validate = models.URLField(max_length=255)
	url_callback_reset = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def json_import(jsondata):
		return generic_json_import(RemoteChallengePin, jsondata)

	def json_import_list(jsondata):
		return generic_json_import_list(RemoteChallengePin, jsondata)

	def save(self, **kwargs):

		host = config.MASTER_HOSTNAME
		port = (config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or '')
		game_slug = self.challenge.room.escapegame.slug
		room_slug = self.challenge.room.slug
		chall_slug = self.challenge.slug

		self.url_callback_validate = 'http://%s%s/web/%s/%s/%s/validate/' % (host, port, game_slug, room_slug, chall_slug)
		self.url_callback_reset = 'http://%s%s/web/%s/%s/%s/reset/' % (host, port, game_slug, room_slug, chall_slug)

		super(RemoteChallengePin, self).save(**kwargs)

class RemoteDoorPin(models.Model):

	name = models.CharField(max_length=255)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	url_callback_lock = models.URLField(max_length=255)
	url_callback_unlock = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def json_import(jsondata):
		return generic_json_import(RemoteDoorPin, jsondata)

	def json_import_list(jsondata):
		return generic_json_import_list(RemoteDoorPin, jsondata)

	def save(self, **kwargs):

		host = config.MASTER_HOSTNAME
		port = (config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or '')
		game_slug = self.room.escapegame.slug
		room_slug = self.room.slug

		self.url_callback_lock = 'http://%s%s/web/%s/%s/lock/' % (host, port, game_slug, room_slug)
		self.url_callback_unlock = 'http://%s%s/web/%s/%s/unlock/' % (host, port, game_slug, room_slug)

		super(RemoteDoorPin, self).save(**kwargs)

class RemoteLedPin(models.Model):

	name = models.CharField(max_length=255)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	pin_number = models.IntegerField(default=7)
	url_on = models.URLField(max_length=255)
	url_off = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def json_import(jsondata):
		return generic_json_import(RemoteLedPin, jsondata)

	def json_import_list(jsondata):
		return generic_json_import_list(RemoteLedPin, jsondata)

	def save(self, **kwargs):

		host = self.raspberrypi.hostname
		port = (self.raspberrypi.port != 80 and ':%d' % self.raspberrypi.port or '')

		self.url_on = 'http://%s%s/api/led/on/%d/' % (host, port, self.pin_number)
		self.url_off = 'http://%s%s/api/led/off/%d/' % (host, port, self.pin_number)

		super(RemoteLedPin, self).save(**kwargs)

