# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from escapegame import libraspi
from multimedia.models import Image, Video
from controllers.models import RaspberryPi, ChallengeGPIO, DoorGPIO, LiftGPIO

from datetime import timedelta
import traceback


# Escape game classes

class EscapeGame(models.Model):

	from_shell = False

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	time_limit = models.DurationField(default=timedelta(hours=1))
	controller = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)

	cube_delay = models.DurationField(default=timedelta(seconds=30))

	winners_video = models.ForeignKey(Video, null=True, on_delete=models.SET_NULL, related_name='escapegame_winners_video')
	losers_video = models.ForeignKey(Video, null=True, on_delete=models.SET_NULL, related_name='escapegame_losers_video')

	map_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')

	def __str__(self):
		return 'Escape Game - %s' % self.name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if self.slug is None or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(EscapeGame, self).save(*args, **kwargs)

	def get_max_unlock_time(self, rooms):

		if not rooms:
			print("Room list is empty!")
			return None

		for room in rooms:
			if room.door.unlocked_at is None:
				print("WTF we found a locked door! %s %s" % (room, room.door))
				return None

		max_unlock_time_room = max(rooms, key=lambda x: x.door.unlocked_at)

		return max_unlock_time_room.door.unlocked_at

	def finish(self, controller):

		start_time = self.get_max_unlock_time(EscapeGameRoom.objects.filter(game=self, starts_the_timer=True))
		finish_time = self.get_max_unlock_time(EscapeGameRoom.objects.filter(game=self, stops_the_timer=True))

		time_diff = finish_time - start_time
		win = time_diff <= self.time_limit

		video = None

		if self.winners_video and win:
			video = self.winners_video

		elif self.losers_video and not win:
			video = self.losers_video

		if video is not None:
			video_url = video.get_action_url(controller)
			print("Playing ending video: %s" % video_url)
			libraspi.do_get(video_url)

	def reset(self):

		lifts = LiftGPIO.objects.filter(game=self)
		for lift in lifts:
			lift.reset()

		rooms = EscapeGameRoom.objects.filter(game=self)
		for room in rooms:
			room.reset()

		# Some rooms, doors, or challenges might eventually be shared between escape games, so instead
		# of just notifying this game frontend, notify all game frontends just in case.
		libraspi.notify_frontend()
		libraspi.notify_frontend(self, '0:00:00')

	def get_challenges(self):

		challenges = []
		rooms = EscapeGameRoom.objects.filter(game=self)
		for room in rooms:
			challs = EscapeGameChallenge.objects.filter(room=room)
			for chall in challs:
				challenges.append(chall)

		return challenges

	def get_videos(self):

		videos = []

		try:
			lifts = LiftGPIO.objects.filter(game=self)

			for lift in lifts:
				videos.append(lift.briefing_video)

		except LiftGPIO.DoesNotExist:
			pass

		if self.winners_video is not None:
			videos.append(self.winners_video)

		if self.losers_video is not None:
			videos.append(self.losers_video)

		challs = self.get_challenges()
		for chall in challs:
			if chall.solved_video is not None:
				videos.append(chall.solved_video)

		return videos

	def get_controllers(self, as_dict=False):
		if as_dict:
			return [ x for x in RaspberryPi.objects.filter(game=None).values() ] + [ x for x in RaspberryPi.objects.filter(game=self).values() ]

		return [ x for x in RaspberryPi.objects.filter(game=None) ] + [ x for x in RaspberryPi.objects.filter(game=self) ]

	class Meta:
		ordering = [ 'name' ]

class EscapeGameCube(models.Model):

	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	tag_id = models.CharField(max_length=8, default="FFFFFFFF")

	def __str__(self):
		return 'Cube - %s - %s' % (self.game.name, self.tag_id)

	# TODO write clean method to validate hex input for tag_id
class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	controller = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE, blank=True, null=True)

	starts_the_timer = models.BooleanField(default=False)
	stops_the_timer = models.BooleanField(default=False)

	door = models.ForeignKey(DoorGPIO, null=True, on_delete=models.CASCADE, related_name='room_door')

	room_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	def __str__(self):
		return 'Room - %s - %s' % (self.game.name, self.name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		if self.door is None:
			name = 'Exit Door - %s' % self.name
			door = DoorGPIO(name=name, controller=self.get_controller(), image=self.door_image)
			door.save()
			self.door = door

		self.clean()
		super(EscapeGameRoom, self).save(*args, **kwargs)

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

		# TODO reset cubes
		#if self.cube is not None:
		#	self.cube.reset()

		self.door.reset()

		challs = EscapeGameChallenge.objects.filter(room=self)
		for chall in challs:
			chall.reset()

	class Meta:
		ordering = [ 'id', 'game', 'name' ]

class EscapeGameChallenge(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)

	gpio = models.ForeignKey(ChallengeGPIO, null=True, on_delete=models.CASCADE, related_name='challenge_gpio')
	dependent_on = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

	solved_video = models.ForeignKey(Video, blank=True, null=True, on_delete=models.SET_NULL, related_name='solved_video')

	challenge_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_image')
	challenge_solved_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_solved_image')

	callback_url_solve = models.URLField(default='')
	callback_url_reset = models.URLField(default='')

	def __str__(self):
		return 'Challenge - %s / %s / %s' % (self.room.game.name, self.room.name, self.name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		lang = 'en'
		raspi = RaspberryPi.get_myself()
		host, port, protocol = libraspi.get_net_info(raspi)

		base_url = '%s://%s%s/%s/api/challenge/%s/%s/%s' % (protocol, host, port, lang, self.room.game.slug, self.room.slug, self.slug)

		self.callback_url_solve = '%s/validate/' % base_url
		self.callback_url_reset = '%s/reset/' % base_url

		self.clean()
		super(EscapeGameChallenge, self).save(*args, **kwargs)

		if self.gpio is None:
			name = 'GPIO - %s' % self.name
			controller = self.room.controller or self.room.game.controller
			gpio = ChallengeGPIO(name=name, controller=controller)
			gpio.save()
			self.gpio = gpio
			super(EscapeGameChallenge, self).save(*args, **kwargs)

	def get_controller(self):

		if self.gpio is not None and self.gpio.controller is not None:
			return self.gpio.controller

		return self.room.controller or self.room.game.controller

	def reset(self):
		self.gpio.reset()
		self.save()

		try:
			doors = DoorGPIO.objects.filter(dependent_on=self)

		except DoorGPIO.DoesNotExist:
			doors = []

		for door in doors:
			door.reset()

	def check_solved(self):

		if self.dependent_on is not None and self.dependent_on.gpio.solved_at is None:
			return False

		return self.gpio.check_solved()

	def set_solved(self, request, action):
		try:
			solved = (action == 'validate')
			actionstr = (solved and 'Solving' or 'Reseting')
			print('%s challenge %s / %s / %s' % (actionstr, self.room.game.name, self.room.name, self.name))

			status, message = (solved and self.gpio.solve() or self.gpio.reset())
			if status != 0:
				raise Exception(message)

			controller = self.get_controller()

			if self.gpio.solved:

				# If we have an associated video, play it remotely on the controller of this challenge
				if self.solved_video is not None:
					video_url = self.solved_video.get_action_url(controller)
					print("Solved video: %s" % video_url)
					libraspi.do_get(video_url)

				# Open extra doors with a dependency on me
				try:
					extra_doors = DoorGPIO.objects.filter(dependent_on=self)

				except DoorGPIO.DoesNotExist:
					extra_doors = []

				for extra_door in extra_doors:

					status, message = extra_door.forward_lock_request(request, self.room.game, self.room, 'unlock')
					if status != 0:
						raise Exception(message)

			# Was this the last challenge to solve in this room?
			if self.room.all_challenge_validated():

				print('This was the last remaining challenge to solve, opening door for %s' % self.room.name)
				status, message = self.room.door.forward_lock_request(request, self.room.game, self.room, 'unlock')
				if status != 0:
					raise Exception(message)

				# Was this the last room of this game?
				if self.room.is_last_room():

					print('This was the last room, finishing escape game')
					self.room.game.finish(controller)

				else:
					print('Still some rooms to explore')
			else:
				print('Still unsolved challenge in room %s' % self.room.name)

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s\n\n%s' % (err, traceback.format_exc())

	class Meta:
		ordering = [ 'id', 'room', 'name' ]
