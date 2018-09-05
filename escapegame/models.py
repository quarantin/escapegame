# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from constance import config

from escapegame import libraspi

from multimedia.models import *

from controllers.models import *

from datetime import timedelta

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

	cube   = models.ForeignKey(Cube, null=True, on_delete=models.CASCADE, related_name='escapegame_cube')
	cube_2 = models.ForeignKey(Cube, null=True, on_delete=models.CASCADE, related_name='escapegame_cube_2', blank=True)

	cube_delay = models.DurationField(default=timedelta(seconds=30))

	briefing_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_briefing_video')
	winners_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_winners_video')
	losers_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_losers_video')

	start_time = models.DateTimeField(blank=True, null=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	map_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')

	def __str__(self):
		return 'Escape Game - %s' % self.escapegame_name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.escapegame_name)
		if self.slug is None or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(EscapeGame, self).save(*args, **kwargs)
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

		self.cube.reset()

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

	cube = models.ForeignKey(Cube, null=True, on_delete=models.CASCADE, related_name='room_cube', blank=True)

	door = models.ForeignKey(Door, null=True, on_delete=models.CASCADE, related_name='room_door')
	door_pin = models.IntegerField(default=10)

	room_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	def __str__(self):
		return 'Room - %s - %s' % (self.escapegame.escapegame_name, self.room_name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.room_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		if self.door is None:
			name = 'Exit Door - %s' % self.room_name
			door = Door(name=name, raspberrypi=self.get_controller(), pin=self.door_pin)
			door.save()
			self.door = door

		self.clean()
		super(EscapeGameRoom, self).save(*args, **kwargs)
		libraspi.notify_frontend(self.escapegame)

	def all_challenge_validated(self):
		try:
			valid = True
			challs = EscapeGameChallenge.objects.filter(room=self)
			for chall in challs:
				if not chall.gpio.solved:
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

		if self.cube is not None:
			self.cube.reset()

		self.door.reset()

		challs = EscapeGameChallenge.objects.filter(room=self)
		for chall in challs:
			chall.reset()

	class Meta:
		ordering = [ 'id', 'escapegame', 'room_name' ]

class EscapeGameChallenge(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	challenge_name = models.CharField(max_length=255, unique=True)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	gpio = models.ForeignKey(Challenge, null=True, on_delete=models.CASCADE, related_name='challenge_gpio')
	gpio_pin = models.IntegerField(default=31)

	solved_video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL, related_name='solved_video')

	challenge_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_image')
	challenge_solved_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_solved_image')

	def __str__(self):
		return 'Challenge - %s / %s / %s' % (self.room.escapegame.escapegame_name, self.room.room_name, self.challenge_name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.challenge_name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		if self.gpio is None:
			name = 'Challenge - %s' % self.challenge_name
			gpio = Challenge(name=name, raspberrypi=self.get_controller(), pin=self.gpio_pin)
			gpio.save()
			self.gpio = gpio

		self.clean()
		super(EscapeGameChallenge, self).save(*args, **kwargs)
		libraspi.notify_frontend(self.room.escapegame)

	def get_controller(self):
		return self.room.get_controller()

	def reset(self):
		self.gpio.reset()
		self.save()

	def set_solved(self, request, solved):
		try:
			action = (solved and 'Solving' or 'Reseting')
			print('%s challenge %s / %s / %s' % (action, self.room.escapegame.escapegame_name, self.room.room_name, self.challenge_name))

			status, message = (solved and self.gpio.solve() or self.gpio.reset())
			if status != 0:
				return status, 'Error: %s' % message

			if self.gpio.solved and self.solved_video:
				self.solved_video.play()

			# Was this the last challenge to solve in this room?
			if self.room.all_challenge_validated():

				print('This was the last remaining challenge to solve, opening door for %s' % self.room.room_name)
				self.room.door.unlock()

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
