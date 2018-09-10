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
	name = models.CharField(max_length=255, unique=True)
	time_limit = models.DurationField(default=timedelta(hours=1))
	controller = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE, related_name='escapegame_controller')

	cube   = models.ForeignKey(CubeGPIO, null=True, on_delete=models.CASCADE, related_name='escapegame_cube')
	cube_2 = models.ForeignKey(CubeGPIO, null=True, on_delete=models.CASCADE, related_name='escapegame_cube_2', blank=True)

	cube_delay = models.DurationField(default=timedelta(seconds=30))

	briefing_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_briefing_video')
	winners_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_winners_video')
	losers_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE, related_name='escapegame_losers_video')

	start_time = models.DateTimeField(blank=True, null=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	map_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')

	def __str__(self):
		return 'Escape Game - %s' % self.name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
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

		doors = DoorGPIO.objects.filter(game=self)
		for door in doors:
			door.reset()

		rooms = EscapeGameRoom.objects.filter(game=self)
		for room in rooms:
			room.reset()

	def get_challenges(self, controller=None):

		if not controller:
			controller = self.controller

		challenges = []
		rooms = EscapeGameRoom.objects.filter(game=self)
		for room in rooms:
			challs = EscapeGameChallenge.objects.filter(room=room)
			for chall in challs:
				if chall.get_controller() == controller:
					challenges.append(chall)

		return challenges

	def get_videos(self, controller=None):

		videos = []

		if self.briefing_video is not None:
			videos.append(self.briefing_video)

		if self.winners_video is not None:
			videos.append(self.winners_video)

		if self.losers_video is not None:
			videos.append(self.losers_video)

		challs = self.get_challenges(controller)
		for chall in challs:
			if chall.solved_video is not None:
				videos.append(chall.solved_video)

		return videos

	class Meta:
		ordering = [ 'name' ]

class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	controller = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE, blank=True, null=True)

	is_sas = models.BooleanField(default=False)

	cube = models.ForeignKey(CubeGPIO, null=True, on_delete=models.CASCADE, related_name='room_cube', blank=True)

	door = models.ForeignKey(DoorGPIO, null=True, on_delete=models.CASCADE, related_name='room_door')
	door_pin = models.IntegerField(default=11)

	room_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	def __str__(self):
		return 'Room - %s - %s' % (self.game.name, self.name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		if self.controller is None:
			self.controller = self.game.controller

		if self.door is None:
			name = 'Exit Door - %s' % self.name
			door = DoorGPIO(name=name, controller=self.get_controller(), image=self.door_image, action_pin=self.door_pin)
			door.save()
			self.door = door

		self.clean()
		super(EscapeGameRoom, self).save(*args, **kwargs)
		libraspi.notify_frontend(self.game)

	def all_challenge_validated(self):
		try:
			valid = True
			challs = EscapeGameChallenge.objects.filter(room=self)
			for chall in challs:
				if chall.gpio.solved_at is None:
					valid = False

			return valid

		except Exception as err:
			print('Error: %s' % err)
			return False

	def is_last_room(self):
		last_room = EscapeGameRoom.objects.filter(game=self.game).order_by('id').last()
		return last_room == self

	def get_controller(self):
		return self.controller or self.game.controller

	def reset(self):

		if self.cube is not None:
			self.cube.reset()

		self.door.reset()

		challs = EscapeGameChallenge.objects.filter(room=self)
		for chall in challs:
			chall.reset()

	def lock(self):
		status, message = self.door.lock()
		libraspi.notify_frontend(self.game)
		return status, message

	def unlock(self):
		status, message = self.door.unlock()
		libraspi.notify_frontend(self.game)
		return status, message

	class Meta:
		ordering = [ 'id', 'game', 'name' ]

class EscapeGameChallenge(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	gpio = models.ForeignKey(ChallengeGPIO, null=True, on_delete=models.CASCADE, related_name='challenge_gpio')
	gpio_pin = models.IntegerField(default=31)

	solved_video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL, related_name='solved_video')

	challenge_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_image')
	challenge_solved_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_solved_image')

	def __str__(self):
		return 'Challenge - %s / %s / %s' % (self.room.game.name, self.room.name, self.name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		if self.gpio is None:
			name = 'Challenge - %s' % self.name
			gpio = ChallengeGPIO(name=name, controller=self.get_controller(), action_pin=self.gpio_pin)
			gpio.save()
			self.gpio = gpio

		if self.gpio_pin != self.gpio.action_pin:
			self.gpio.action_pin = self.gpio_pin
			self.gpio.save()

		self.clean()
		super(EscapeGameChallenge, self).save(*args, **kwargs)
		libraspi.notify_frontend(self.room.game)

	def get_controller(self):
		return self.room.get_controller()

	def reset(self):
		self.gpio.reset()
		self.save()

	def set_solved(self, request, solved):
		try:
			action = (solved and 'Solving' or 'Reseting')
			print('%s challenge %s / %s / %s' % (action, self.room.game.name, self.room.name, self.name))

			status, message = (solved and self.gpio.solve() or self.gpio.reset())
			if status != 0:
				return status, 'Error: %s' % message

			if self.gpio.solved and self.solved_video:
				self.solved_video.play()

			# Was this the last challenge to solve in this room?
			if self.room.all_challenge_validated():

				print('This was the last remaining challenge to solve, opening door for %s' % self.room.name)
				self.room.door.unlock()

				# Was this the last room of this game?
				if self.room.is_last_room():

					print('This was the last room, stopping escape game counter')
					self.room.game.finish(request)

				else:
					print('Still some rooms to explore')
			else:
				print('Still unsolved challenge in room %s' % self.room.name)

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % err

	class Meta:
		ordering = [ 'id', 'room', 'name' ]
