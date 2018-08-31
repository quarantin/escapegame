# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

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


# Escape game classes

class EscapeGame(models.Model):

	slug = models.SlugField(max_length=255)
	escapegame_name = models.CharField(max_length=255, default='')
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL, related_name='escapegame_raspberrypi')
	video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL, related_name='escapegame_video')

	cube_pin = models.IntegerField(default=7)
	cube_delay = models.IntegerField(default=50)
	cube_raised = models.BooleanField(default=False)

	map_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')

	start_time = models.DateTimeField(blank=True, null=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.escapegame_name

	def clean(self):
		if not libraspi.is_valid_pin(self.cube_pin):
			raise ValidationError({
				'cube_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.cube_pin,
			})

	def save(self, **kwargs):
		self.slug = slugify(self.escapegame_name)
		self.clean()
		super(EscapeGame, self).save(**kwargs)

	def finish(self):
		self.finish_time = timezone.localtime()
		self.save()

	def reset(self):
		self.start_time = None
		self.finish_time = None
		# TODO lower the cube
		rooms = EscapeGameRoom.objects.filter(escapegame=self)
		for room in rooms:
			room.reset()

	def get_controller(self):
		return self.raspberrypi

class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255)
	room_name = models.CharField(max_length=255, default='')
	escapegame = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, blank=True, null=True, on_delete=models.SET_NULL)
	has_cube = models.BooleanField(default=False)

	door_pin = models.IntegerField(default=11)
	door_locked = models.BooleanField(default=True)

	room_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	unlock_time = models.DateTimeField(blank=True, null=True)

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

	def reset(self):
		self.unlock_time = None
		self.set_door_locked(True)
		# TODO lower the cube
		challs = EscapeGameChallenge.objects.filter(room=self)
		for chall in challs:
			chall.reset()

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

			libraspi.notify_frontend(self.escapegame)

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

	solved_time = models.DateTimeField(blank=True, null=True)

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

	def reset(self):
		self.solved = False
		self.solved_time = None
		self.save()

	def set_solved(self, solved):
		try:
			action = (solved and 'Solving' or 'Reseting')
			print('%s challenge %s / %s / %s' % (action, self.room.escapegame.escapegame_name, self.room.room_name, self.challenge_name))
			self.solved = solved
			self.save()

			if self.solved:
				self.solved_time = timezone.localtime()
				if self.video:
					libraspi.video_control('play', video)

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

			libraspi.notify_frontend(self.room.escapegame)

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % err
