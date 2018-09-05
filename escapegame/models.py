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

	from_shell = False

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	escapegame_name = models.CharField(max_length=255, unique=True)
	time_limit = models.DurationField()
	raspberrypi = models.ForeignKey(RaspberryPi, null=True, on_delete=models.CASCADE, related_name='escapegame_raspberrypi')

	cube_pin = models.IntegerField(default=7)
	cube_delay = models.IntegerField(default=50)
	cube_raised = models.BooleanField(default=False)

	briefing_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_briefing_video')
	winners_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_winners_video')
	losers_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_losers_video')

	start_time = models.DateTimeField(blank=True, null=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	map_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')

	def __str__(self):
		return 'Escape Game - %s' % self.escapegame_name

	def clean(self):
		if not libraspi.is_valid_pin(self.cube_pin):
			raise ValidationError({
				'cube_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.cube_pin,
			})

	def save(self, **kwargs):
		new_slug = slugify(self.escapegame_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(EscapeGame, self).save(**kwargs)
		libraspi.notify_frontend(self)

	def finish(self, request):
		if not self.finish_time:
			self.finish_time = timezone.localtime()
			self.save()

			time_diff = self.finish_time - self.start_time
			if self.losers_video and time_diff > self.time_limit:
				self.losers_video.control(request, 'play')

			if self.winners_video and time_diff <= self.time_limit:
				self.winners_video.control(request, 'play')

	def reset(self):
		self.start_time = None
		self.finish_time = None
		self.save()
		# TODO lower the cube in the briefing room
		rooms = EscapeGameRoom.objects.filter(escapegame=self)
		for room in rooms:
			room.reset()

	def get_challenges(self, controller=None):

		if not controller:
			controller = self.raspberrypi

		challenges = []
		rooms = EscapeGameRoom.objects.filter(escapegame=self)
		for room in rooms:
			challs = EscapeGameChallenge.objects.filter(room=room)
			for chall in challs:
				if chall.get_controller() == controller:
					challenges.append(chall)

		return challenges

	class Meta:
		ordering = [ 'escapegame_name' ]

class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	room_name = models.CharField(max_length=255, unique=True)
	escapegame = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, null=True, on_delete=models.CASCADE)
	has_cube = models.BooleanField(default=False)

	door_pin = models.IntegerField(default=11)
	door_locked = models.BooleanField(default=True)
	unlock_time = models.DateTimeField(blank=True, null=True)

	room_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	def __str__(self):
		return 'Room - %s - %s' % (self.escapegame.escapegame_name, self.room_name)

	def clean(self):
		if not libraspi.is_valid_pin(self.door_pin):
			raise ValidationError({
				'door_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.door_pin,
			})

	def save(self, **kwargs):
		new_slug = slugify(self.room_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(EscapeGameRoom, self).save(**kwargs)
		libraspi.notify_frontend(self.escapegame)

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
		return self.raspberrypi or self.escapegame.raspberrypi

	def reset(self):
		self.unlock_time = None
		self.set_door_locked(True)
		self.save()
		# TODO lower the cube in this room
		challs = EscapeGameChallenge.objects.filter(room=self)
		for chall in challs:
			chall.reset()

	def set_door_locked(self, locked):
		try:
			print('EscapeGameRoom.set_door_locked(%s) [%s]' % (locked, self))
			action = (locked and 'lock' or 'unlock')

			status, message = libraspi.door_control(action, self)
			if status == 0:
				self.door_locked = locked

				action = (locked and 'Closing' or 'Opening')
				print("%s door of room `%s / %s`" % (action, self.escapegame, self.room_name))

				if not locked and not self.unlock_time:
					self.unlock_time = timezone.localtime()

				self.save()

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

	class Meta:
		ordering = [ 'id', 'escapegame', 'room_name' ]

class EscapeGameChallenge(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	challenge_name = models.CharField(max_length=255, unique=True)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	challenge_pin = models.IntegerField(default=31)
	solved = models.BooleanField(default=False)
	solved_time = models.DateTimeField(blank=True, null=True)
	solved_video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL, related_name='solved_video')

	challenge_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_image')
	challenge_solved_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_solved_image')

	def __str__(self):
		return 'Challenge - %s / %s / %s' % (self.room.escapegame.escapegame_name, self.room.room_name, self.challenge_name)

	def clean(self):
		if not libraspi.is_valid_pin(self.challenge_pin):
			raise ValidationError({
				'challenge_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.challenge_pin,
			})

	def save(self, **kwargs):
		new_slug = slugify(self.challenge_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(EscapeGameChallenge, self).save(**kwargs)
		libraspi.notify_frontend(self.room.escapegame)

	def get_controller(self):
		return self.room.get_controller()

	def reset(self):
		self.solved = False
		self.solved_time = None
		self.save()

	def set_solved(self, request, solved):
		try:
			action = (solved and 'Solving' or 'Reseting')
			print('%s challenge %s / %s / %s' % (action, self.room.escapegame.escapegame_name, self.room.room_name, self.challenge_name))

			self.solved = solved

			if self.solved and not self.solved_time:
				self.solved_time = timezone.localtime()

			self.save()

			if self.solved and self.solved_video:
				self.solved_video.control(request, 'play')

			# Was this the last challenge to solve in this room?
			if self.room.all_challenge_validated():

				print('This was the last remaining challenge to solve, opening door for %s' % self.room.room_name)
				self.room.set_door_locked(False)

				# Was this the last room of this game?
				if self.room.is_last_room():

					print('This was the last room, stopping escape game counter')
					self.room.escapegame.finish(request)

				else:
					print('Still some rooms to explore')
			else:
				print('Still unsolved challenge in room %s' % self.room.room_name)

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % err

	class Meta:
		ordering = [ 'id', 'room', 'challenge_name' ]
