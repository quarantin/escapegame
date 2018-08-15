# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from constance import config

from escapegame import libraspi

from multimedia.models import *

from controllers.models import *

from jsonexport.decorators import json_import

from escapegame.apps import EscapegameConfig as AppConfig
logger = AppConfig.logger


# Escape game classes

@json_import
class EscapeGame(models.Model):

	slug = models.SlugField(max_length=255)
	escapegame_name = models.CharField(max_length=255, default='')
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.CASCADE)
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

	def save(self, **kwargs):
		self.slug = slugify(self.escapegame_name)
		super(EscapeGame, self).save(**kwargs)

	def set_door_locked(self, door_pin, locked):
		try:
			if door_pin not in [ self.sas_door_pin, self.corridor_door_pin ]:
				raise Exception('Invalid door pin: %d' % door_pin)

			status, message = libraspi.set_door_locked(door_pin, locked)
			if status == 0:

				if door_pin == self.sas_door_pin:
					self.sas_door_locked = locked
				elif door_pin == self.corridor_door_pin:
					self.corridor_door_locked = locked

				self.save()

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

@json_import
class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255)
	room_name = models.CharField(max_length=255, default='')
	escapegame = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.CASCADE)

	door_pin = models.IntegerField(default=5)
	door_locked = models.BooleanField(default=True)

	room_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_image_path', limit_choices_to={ 'image_type': Image.TYPE_ROOM })
	door_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='room_door_image_path', limit_choices_to={ 'image_type': Image.TYPE_DOOR })

	def __str__(self):
		return '%s / %s' % (self.escapegame, self.room_name)

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

@json_import
class EscapeGameChallenge(models.Model):

	slug = models.SlugField(max_length=255)
	challenge_name = models.CharField(max_length=255, default='')
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	challenge_pin = models.IntegerField(default=31)
	solved = models.BooleanField(default=False)

	challenge_image_path = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name='chall_map_image_path', limit_choices_to={ 'image_type': Image.TYPE_CHALL })

	def __str__(self):
		return '%s / %s' % (self.room, self.challenge_name)

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
