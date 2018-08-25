# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from constance import config

from escapegame import libraspi

from multimedia.models import *

from controllers.models import *

from jsonexport.decorators import json_import

from PIL import Image as PIL

from io import BytesIO

from escapegame.apps import EscapegameConfig as AppConfig
logger = AppConfig.logger

def paste_image(to_image, from_image_field):
	from_image = PIL.open(from_image_field.image_path.path)
	to_image.paste(from_image, (0, 0), from_image)

# Escape game classes

@json_import
class EscapeGame(models.Model):

	slug = models.SlugField(max_length=255)
	escapegame_name = models.CharField(max_length=255, default='')
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL, related_name='escapegame_raspberrypi')
	video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL)

	sas_door_pin = models.IntegerField(default=7)
	corridor_door_pin = models.IntegerField(default=10)

	sas_door_locked = models.BooleanField(default=True)
	corridor_door_locked = models.BooleanField(default=True)

	map_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')
	sas_door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='sas_door_image')
	corridor_door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='corridor_door_image')

	start_time = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.escapegame_name

	def save(self, **kwargs):
		self.slug = slugify(self.escapegame_name)
		super(EscapeGame, self).save(**kwargs)

	def notify_frontend(self, message='notify'):
		redis_publisher = RedisPublisher(facility='notify', broadcast=True)
		redis_publisher.publish_message(RedisMessage(message))

	def get_door_pin(self, slug):
		if slug == 'sas':
			return self.sas_door_pin

		elif slug == 'corridor':
			return self.corridor_door_pin

		raise Exception('Invalid door `%s`' % slug)

	def set_door_locked(self, door_pin, locked):
		try:
			if type(door_pin) is str:
				door_pin = self.get_door_pin(door_pin)

			if door_pin not in [ self.sas_door_pin, self.corridor_door_pin ]:
				raise Exception('Invalid door pin: %d' % door_pin)

			print('EscapeGame.set_door_locked(%d, %s) [%s]' % (door_pin, locked, self))
			action = (locked and 'lock' or 'unlock')
			status, message = libraspi.door_control(action, self, door_pin)
			if status == 0:

				action = (locked and 'Closing' or 'Opening')

				if door_pin == self.sas_door_pin:
					self.sas_door_locked = locked
					print("%s SAS door of escape game `%s`" % (action, self.escapegame_name))

				elif door_pin == self.corridor_door_pin:
					self.corridor_door_locked = locked
					print("%s corridor door of escape game `%s`" % (action, self.escapegame_name))

				if locked == False:
					self.start_time = timezone.localtime()

				self.save()
				self.notify_frontend()

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

@json_import
class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255)
	room_name = models.CharField(max_length=255, default='')
	escapegame = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL)

	door_pin = models.IntegerField(default=5)
	door_locked = models.BooleanField(default=True)

	room_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	start_time = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return '%s / %s' % (self.escapegame, self.room_name)

	def save(self, **kwargs):
		self.slug = slugify(self.room_name)
		super(EscapeGameRoom, self).save(**kwargs)

	def set_door_locked(self, locked):
		try:
			print('EscapeGameRoom.set_door_locked(%s) [%s]' % (locked, self))
			action = (locked and 'lock' or 'unlock')
			status, message = libraspi.door_control(action, self, self.door_pin)
			if status == 0:
				self.door_locked = locked

				action = (locked and 'Closing' or 'Opening')
				print("%s door of room `%s / %s`" % (action, self.escapegame, self.room_name))

				if locked == False:
					self.start_time = timezone.localtime()

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

	challenge_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_image')
	challenge_solved_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_solved_image')

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
