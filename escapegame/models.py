# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from constance import config

from escapegame import libraspi

from multimedia.models import *

from controllers.models import *

from PIL import Image as PIL

from io import BytesIO

from escapegame.apps import EscapegameConfig as AppConfig
logger = AppConfig.logger


def paste_image(to_image, from_image_field):
	from_image = PIL.open(from_image_field.image_path.path)
	to_image.paste(from_image, (0, 0), from_image)

def notify_frontend(game, message='notify'):

	facility = 'notify-%s' % game.slug

	redis_publisher = RedisPublisher(facility=facility, broadcast=True)
	redis_publisher.publish_message(RedisMessage(message))
	print('notify_frontend("%s")' % message)


# Escape game classes

class EscapeGame(models.Model):

	slug = models.SlugField(max_length=255)
	escapegame_name = models.CharField(max_length=255, default='')
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL, related_name='escapegame_raspberrypi')
	video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL, related_name='escapegame_video')

	cube_delay = models.IntegerField(default=50)

	cube_pin = models.IntegerField(default=7)
	sas_door_pin = models.IntegerField(default=11)
	corridor_door_pin = models.IntegerField(default=12)

	cube_raised = models.BooleanField(default=False)
	sas_door_locked = models.BooleanField(default=True)
	corridor_door_locked = models.BooleanField(default=True)

	map_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')
	sas_door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='sas_door_image')
	corridor_door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='corridor_door_image')

	start_time = models.DateTimeField(blank=True, null=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.escapegame_name

	def clean(self):

		if not libraspi.is_valid_pin(self.cube_pin):
			raise ValidationError({
				'sas_door_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.cube_pin,
			})

		if not libraspi.is_valid_pin(self.sas_door_pin):
			raise ValidationError({
				'sas_door_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.sas_door_pin,
			})

		if not libraspi.is_valid_pin(self.corridor_door_pin):
			raise ValidationError({
				'corridor_door_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.corridor_door_pin,
			})

	def save(self, **kwargs):
		self.slug = slugify(self.escapegame_name)
		self.clean()
		super(EscapeGame, self).save(**kwargs)

	def finish(self):
		self.finish_time = timezone.localtime()
		self.save()

	def get_door_pin(self, slug):
		if slug == 'sas':
			return self.sas_door_pin

		elif slug == 'corridor':
			return self.corridor_door_pin

		raise Exception('Invalid door `%s`' % slug)

	def get_controller(self):
		return self.raspberrypi

	def set_door_locked(self, door_pin, locked):
		try:
			if type(door_pin) is str:
				door_pin = self.get_door_pin(door_pin)

			if door_pin not in [ self.sas_door_pin, self.corridor_door_pin ]:
				raise Exception('Invalid door pin: %d' % door_pin)

			print('EscapeGame.set_door_locked(%d, %s) [%s]' % (door_pin, locked, self))
			action = (locked and 'lock' or 'unlock')
			status, message = libraspi.door_control(action, None, door_pin)
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

			notify_frontend(self)

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255)
	room_name = models.CharField(max_length=255, default='')
	escapegame = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL)

	door_pin = models.IntegerField(default=11)
	door_locked = models.BooleanField(default=True)

	room_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	start_time = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return '%s / %s' % (self.escapegame, self.room_name)

	def clean(self):
		if not libraspi.is_valid_pin(self.door_pin):
			raise ValidationError({
				'door_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.door_pin,
			})

	def save(self, **kwargs):
		self.slug = slugify(self.room_name)
		self.clean()
		super(EscapeGameRoom, self).save(**kwargs)

	def all_challenge_validated(self):
		try:
			valid = True
			challs = EscapeGameChallenge.objects.filter(room=self)
			for chall in challs:
				if not chall.solved:
					valid = False

			return valid

		except Exception as err:
			print('Error: %s' % err)
			return False

	def is_last_room(self):
		last_room = EscapeGameRoom.objects.filter(escapegame=self.escapegame).order_by('id').last()
		return last_room == self

	def get_controller(self):
		return self.raspberrypi and self.raspberrypi or self.escapegame.get_controller()

	def set_door_locked(self, locked):
		try:
			print('EscapeGameRoom.set_door_locked(%s) [%s]' % (locked, self))
			action = (locked and 'lock' or 'unlock')
			status, message = libraspi.door_control(action, None, self.door_pin)
			if status == 0:
				self.door_locked = locked

				action = (locked and 'Closing' or 'Opening')
				print("%s door of room `%s / %s`" % (action, self.escapegame, self.room_name))

				if not locked:
					self.start_time = timezone.localtime()

				self.save()

			notify_frontend(self.escapegame)

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

class EscapeGameChallenge(models.Model):

	slug = models.SlugField(max_length=255)
	challenge_name = models.CharField(max_length=255, default='')
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)
	video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_video')

	challenge_pin = models.IntegerField(default=31)
	solved = models.BooleanField(default=False)

	challenge_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_image')
	challenge_solved_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_solved_image')

	def __str__(self):
		return '%s / %s' % (self.room, self.challenge_name)

	def clean(self):
		if not libraspi.is_valid_pin(self.challenge_pin):
			raise ValidationError({
				'challenge_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.challenge_pin,
			})

	def save(self, **kwargs):
		self.slug = slugify(self.challenge_name)
		self.clean()
		super(EscapeGameChallenge, self).save(**kwargs)

	def get_controller(self):
		return self.room.get_controller()

	def set_solved(self, solved):
		try:
			action = (solved and 'Solving' or 'Reseting')
			print('%s challenge %s / %s / %s' % (action, self.room.escapegame.escapegame_name, self.room.room_name, self.challenge_name))
			self.solved = solved
			self.save()

			if self.solved and self.video:
				libraspi.video_control('play', None, video)

			if self.room.all_challenge_validated():
				print('This was the last remaining challenge to solved, opening door for %s' % self.room.room_name)
				self.room.set_door_locked(False)

				if self.room.is_last_room():
					print('This was the last room, stopping escape game counter')
					self.room.escapegame.finish()
				else:
					print('Still some rooms to explore')
			else:
				print('Still some unsolved challenge remaining in room %s' % self.room.room_name)

			notify_frontend(self.room.escapegame)

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % err
