# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
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

	def __str__(self):
		return self.escapegame_name

	def save(self, **kwargs):
		self.slug = slugify(self.escapegame_name)
		super(EscapeGame, self).save(**kwargs)

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

	def draw_map(self):
		try:
			# If this escape game doesn't have a map image, then there is nothing to draw
			if not self.map_image:
				return None

			# Draw the base map with locked door and unsolved challenges
			map_image = PIL.open(self.map_image.image_path.path)

			# Draw SAS door if it's opened
			if not self.sas_door_locked and self.sas_door_image:
				paste_image(map_image, self.sas_door_image)

			# Draw corridor door if it's opened
			if not self.corridor_door_locked and self.corridor_door_image:
				paste_image(map_image, self.corridor_door_image)

			# Draw each room of this escape game onto the map image
			rooms = EscapeGameRoom.objects.filter(escapegame=self)
			for room in rooms:
				room.draw_map(map_image)

			# Prepare a byte buffer
			bytes_io = BytesIO()

			# Save the image to our byte buffer
			map_image.save(bytes_io, 'PNG')

			# Return the content of our byte buffer which is the raw image data
			return bytes_io.getvalue()

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
	door_unlocked_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL, related_name='door_unlocked_image')

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

	def draw_map(self, map_image):

		# Draw room if there's an image for it
		if self.room_image:
			paste_image(map_image, self.room_image)

		# Draw room door if it's unlocked
		if not self.door_locked and self.door_unlocked_image:
			paste_image(map_image, self.door_unlocked_image)

		# Draw each challenge in this room onto the map
		challs = EscapeGameChallenge.objects.filter(room=self)
		for chall in challs:
			chall.draw_map(map_image)

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

	def draw_map(self, map_image):

		# Draw the challenge if there's an image for it
		if self.challenge_image:
			paste_image(map_image, self.challenge_image)

		# Draw the challenge if it's solved
		if self.solved and self.challenge_solved_image:
			paste_image(map_image, self.challenge_solved_image)
