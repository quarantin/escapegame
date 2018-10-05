# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from escapegame import libraspi
from multimedia.models import Image, MultimediaFile
from controllers.models import RaspberryPi, ChallengeGPIO, DoorGPIO, LiftGPIO

from datetime import timedelta
import traceback


# Escape game classes

class EscapeGame(models.Model):

	from_shell = False

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	time_limit = models.DurationField(default=timedelta(hours=1))
	controller = models.ForeignKey('controllers.RaspberryPi', on_delete=models.CASCADE)

	map_image = models.ForeignKey('multimedia.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='game_map_image')

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

		media = None

		cubes = EscapeGameCube.objects.filter(game=self)
		for cube in cubes:

			if cube.winners_media and win:
				media = cube.winners_media

			elif cube.losers_media and not win:
				media = cube.losers_media

			if media is not None:
				media_url = media.get_action_url(controller)
				print("Playing ending media: %s" % media_url)
				libraspi.do_get(media_url)

	def reset(self):

		cubes = EscapeGameCube.objects.filter(game=self)
		for cube in cubes:

			try:
				lift = LiftGPIO.objects.get(cube=cube)
				lift.reset()

			except LiftGPIO.DoesNotExist:
				pass

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

	def get_multimedia_files(self, media_type):

		media_list = []

		try:
			cubes = EscapeGameCube.objects.filter(game=self)
			for cube in cubes:

				if media_type == cube.briefing_media.media_type:
					media_list.append(cube.briefing_media)

				if media_type == cube.losers_media.media_type:
					media_list.append(cube.losers_media)

				if media_type == cube.winners_media.media_type:
					media_list.append(cube.winners_media)

		except EscapeGameCube.DoesNotExist:
			pass

		try:
			extra_media = MultimediaFile.objects.filter(game=self)

			for media in extra_media:
				if media_type == media.media_type:
					media_list.append(media)

		except MultimediaFile.DoesNotExist:
			pass

		challs = self.get_challenges()
		for chall in challs:
			if chall.solved_media is not None and media_type == chall.solved_media.media_type:
				media_list.append(chall.solved_media)

		return set(media_list)

	def get_controllers(self, as_dict=False):
		if as_dict:
			return [ x for x in RaspberryPi.objects.filter(game=None).values() ] + [ x for x in RaspberryPi.objects.filter(game=self).values() ]

		return [ x for x in RaspberryPi.objects.filter(game=None) ] + [ x for x in RaspberryPi.objects.filter(game=self) ]

	class Meta:
		ordering = [ 'name' ]

class EscapeGameCube(models.Model):

	name = models.CharField(max_length=255, unique=True)
	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	tag_id = models.CharField(max_length=8, default="FFFFFFFF")
	cube_delay = models.DurationField(default=timedelta(seconds=30))
	briefing_media = models.ForeignKey('multimedia.MultimediaFile', on_delete=models.CASCADE, related_name='escapegame_cube_briefing_media')
	losers_media = models.ForeignKey('multimedia.MultimediaFile', on_delete=models.CASCADE, related_name='escapegamecube_losers_media')
	winners_media = models.ForeignKey('multimedia.MultimediaFile', on_delete=models.CASCADE, related_name='escapegamecube_winners_media')

	def __str__(self):
		return 'Cube - %s - %s' % (self.name, self.tag_id)

class EscapeGameRoom(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	controller = models.ForeignKey('controllers.RaspberryPi', on_delete=models.CASCADE, blank=True, null=True)

	starts_the_timer = models.BooleanField(default=False)
	stops_the_timer = models.BooleanField(default=False)

	door = models.ForeignKey('controllers.DoorGPIO', null=True, on_delete=models.CASCADE, related_name='room_door')
	has_no_challenge = models.BooleanField(default=False)
	dependent_on = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

	room_image = models.ForeignKey('multimedia.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='room_image')
	door_image = models.ForeignKey('multimedia.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='door_image')

	def __str__(self):
		return 'Room - %s - %s' % (self.game.name, self.name)

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		if self.door is None:
			name = 'Exit Door - %s' % self.name
			door = DoorGPIO(name=name, controller=self.get_controller())
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

	gpio = models.ForeignKey('controllers.ChallengeGPIO', null=True, on_delete=models.CASCADE, related_name='challenge_gpio')
	dependent_on = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

	solved_media = models.ForeignKey('multimedia.MultimediaFile', blank=True, null=True, on_delete=models.SET_NULL, related_name='solved_media')

	challenge_image = models.ForeignKey('multimedia.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_image')
	challenge_solved_image = models.ForeignKey('multimedia.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='challenge_solved_image')

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

			# If this challenge is solved and we have an associated media, play it remotely on the controller of this challenge
			if self.gpio.solved and self.solved_media is not None:
					media_url = self.solved_media.get_action_url(controller)
					print("Solved media: %s - %s" % (self.solved_media.name, media_url))
					libraspi.do_get(media_url)

			# Open rooms with a dependency on my room if it's been opened
			if self.room.door.unlocked_at is not None:

				try:
					dependent_rooms = EscapeGameRoom.objects.filter(dependent_on=self.room)

				except EscapeGameRoom.DoesNotExist:
					dependent_rooms = []

				for dependent_room in dependent_rooms:

					status, message = dependent_room.door.forward_lock_request(request, dependent_room.game, dependent_room, 'unlock')
					if status != 0:
						raise Exception(message)

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s\n\n%s' % (err, traceback.format_exc())

	class Meta:
		ordering = [ 'id', 'room', 'name' ]
