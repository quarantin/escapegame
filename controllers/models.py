# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from constance import config

from multimedia.models import Image
from escapegame import libraspi

import os
import time
import socket


# Controllers classes

class ArduinoSketch(models.Model):

	class Meta:
		verbose_name = 'Arduino Sketch'
		verbose_name_plural = 'Arduino Sketches'

	sketch_name = models.CharField(max_length=255, unique=True)
	sketch_code = models.TextField(max_length=10000)
	sketch_path = models.FileField(upload_to=config.UPLOAD_SKETCH_PATH)

	def __str(self):
		return self.sketch_path.url

	def clean(self):
		if not self.sketch_name:
			raise ValidationError({
				'sketch_name': 'Sketch name cannot be empty',
			})
		if not self.sketch_path:
			raise ValidationError({
				'sketch_path': 'Sketch path cannot be empty',
			})
		if not self.sketch_path.path.lower().endswith('.ino'):
			raise ValidationError({
				'sketch_path': 'An Arduino sketch must have a .ino file extension',
			})

	def save_code(self):

		sketch_path = os.path.join(config.UPLOAD_SKETCH_PATH, self.sketch_path.path)

		if self.sketch_code:
			fin = open(sketch_path, 'w')
			fin.write(self.sketch_code)
			fin.close()

		else:
			fin = open(sketch_path, 'r')
			data = fin.read()
			self.sketch_code = data
			fin.close()

	def save(self, *args, **kwargs):

		# Only true the first time we're called
		if not self.sketch_code:
			super(ArduinoSketch, self).save(*args, **kwargs)

		self.clean()
		self.save_code()
		super(ArduinoSketch, self).save(*args, **kwargs)

class Controller(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	hostname = models.CharField(max_length=255, unique=True)
	port = models.IntegerField(default=80)

	def __str__(self):
		return 'Controller - %s' % self.name

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if not self.slug or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(Controller, self).save(*args, **kwargs)

	def is_myself(self, hostname=None):
		if hostname is None:
			hostname = '%s%s' % (socket.gethostname(), config.MASTER_TLD)

		return hostname == self.hostname

class RaspberryPi(Controller):

	class Meta:
		verbose_name = 'Raspberry Pi'
		verbose_name_plural = 'Raspberry Pis'

	def __str__(self):
		return 'Raspberry Pi - %s' % self.name

	def get_by_name(hostname):
		try:
			return RaspberryPi.objects.get(hostname=hostname)
		except RaspberryPi.DoesNotExist:
			return None

	def get_master():
		return RaspberryPi.get_by_name(config.MASTER_HOSTNAME)

	def get_myself():
		hostname = '%s%s' % (socket.gethostname(), config.MASTER_TLD)
		return RaspberryPi.get_by_name(hostname)

class GPIO(models.Model):

	class Meta:
		verbose_name = 'GPIO'
		verbose_name_plural = 'GPIOs'

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	controller = models.ForeignKey(Controller, null=True, on_delete=models.CASCADE)

	reset_pin = models.IntegerField(default=7)
	action_pin = models.IntegerField(default=11)

	reset_url = models.URLField(max_length=255, blank=True, null=True)
	action_url = models.URLField(max_length=255, blank=True, null=True)

	image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return 'GPIO - %s' % self.name

	def save(self, *args, **kwargs):

		new_slug = slugify(self.name)
		if self.slug is None or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(GPIO, self).save(*args, **kwargs)

	""" Read value from this GPIO
	"""
	def read(self):

		status = 1
		message = 'No action URL or action PIN defined for this GPIO!'
		signal = None

		try:
			if self.action_url is not None:

				status, message, signal = libraspi.do_get(self.action_url)
				if status != 0:
					return -1, mesage, None

			elif self.action_pin is not None:

				status, message, signal = libraspi.get_pin(self.action_pin)
				if status != 0:
					return -1, message, None

			return status, message, signal

		except Exception as err:
			return 1, 'Error: %s' % err, None

	""" Write value to this GPIO
	"""
	def write(self, signal):

		status = 1
		message = 'No action URL or action PIN defined for this GPIO!'

		if self.action_url is not None:

			status, message, html = libraspi.do_get('%s/%d' % (self.action_url, signal and 1 or 0))
			if status != 0:
				return status, message

		elif self.action_pin is not None:

			status, message = libraspi.set_pin(self.action_pin, signal)
			if status != 0:
				return status, message

		return status, message

	""" Reset the state of this GPIO
	"""
	def reset(self):

		status = 1
		message = 'No action URL or action PIN defined for this GPIO!'

		# Call reset URL if one is defined
		if self.reset_url is not None:

			status, message, html = libraspi.do_get(self.reset_url)
			if status != 0:
				return status, message

		# Send reset sequence to reset pin if one is defined
		elif self.reset_pin is not None:

			# Set reset pin to HIGH to trigger controller reset
			status, message = libraspi.set_pin(self.reset_pin, True)
			if status != 0:
				return status, message

			# Wait for the controller to have time to read the value
			time.sleep(0.1)

			# Set reset pin to LOW to stop triggering controller reset
			status, message = libraspi.set_pin(self.reset_pin, False)
			if status != 0:
				return status, message

		return status, message

class ChallengeGPIO(GPIO):

	class Meta:
		verbose_name = 'Challenge GPIO'
		verbose_name_plural = 'Challenge GPIOs'

	challenge = models.ForeignKey('escapegame.EscapeGameChallenge', on_delete=models.CASCADE, blank=True, null=True)

	solved = models.BooleanField(default=False)
	solved_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return 'Challenge GPIO - %s' % self.name

	def save(self, *args, **kwargs):
		self.clean()
		super(ChallengeGPIO, self).save(*args, **kwargs)

	""" Reset this challenge state
	"""
	def reset(self):

		self.solved = False
		self.solved_at = None
		self.save()

		return super(ChallengeGPIO, self).reset()

	""" Callback method to call when this challenge has just been solved
	"""
	def solve(self):
		self.solved = True
		if self.solved_at is None:
			self.solved_at = timezone.localtime()

		self.save()
		return super(ChallengeGPIO, self).write(True)

class CubeGPIO(ChallengeGPIO):

	class Meta:
		verbose_name = 'Cube GPIO'
		verbose_name_plural = 'Cube GPIOs'

	game = models.ForeignKey('escapegame.EscapeGame', on_delete=models.CASCADE)

	tag_id = models.CharField(max_length=32)
	taken_at = models.DateTimeField(blank=True, null=True)
	placed_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return 'Cube GPIO - %s' % self.name

	""" Reset this cube state
	"""
	def reset(self):

		self.taken_at = None
		self.placed_at = None
		self.save()

		status, message = self.lowerStand()
		if status != 0:
			return status, message

		return super(CubeGPIO, self).reset()

	""" Callback method to call when the cube has just been taken from the NFC reader
	"""
	def taken(self):
		if self.taken_time is None:
			self.taken_time = timezone.localtime()
			self.save()
		return 0, 'Success'

	""" Callback method to call when the cube has just been placed on the NFC reader
	"""
	def placed(self):
		if self.placed_time is None:
			self.placed_time = timezone.localtime()
			self.save()
		return 0, 'Success'

	""" Raise the cube stand
	"""
	def raiseStand(self):
		# TODO: Implement me
		return 0, 'Success'

	""" Lower the cube stand
	"""
	def lowerStand(self):
		# TODO: Implement me
		return 0, 'Success'

class DoorGPIO(GPIO):

	class Meta:
		verbose_name = 'Door GPIO'
		verbose_name_plural = 'Door GPIOs'

	game = models.ForeignKey('escapegame.EscapeGame', on_delete=models.CASCADE, blank=True, null=True)
	room = models.ForeignKey('escapegame.EscapeGameRoom', on_delete=models.CASCADE, blank=True, null=True)

	locked = models.BooleanField(default=True)
	unlocked_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return 'Door GPIO - %s' % self.name

	def save(self, *args, **kwargs):
	
		if self.reset_pin is None:
			self.reset_pin = self.action_pin

		self.clean()
		super(DoorGPIO, self).save(*args, **kwargs)

	""" Reset this door state
	"""
	def reset(self):

		self.locked = True
		self.unlocked_at = None
		self.save()

		# Don't call reset from parent because logic is different for doors
		#return super(DoorGPIO, self).reset()
		return super(DoorGPIO, self).write(False)

	""" Lock this door
	"""
	def lock(self):
		print("Locking door `%s`" % self.name)

		self.locked = True
		self.save()

		return super(DoorGPIO, self).write(False)

	""" Unlock this door
	"""
	def unlock(self):
		print("Unlocking door `%s`" % self.name)

		self.locked = False
		if self.unlocked_at is None:
			self.unlocked_at = timezone.localtime()

		self.save()

		return super(DoorGPIO, self).write(True)

	""" Set the state of this door lock
	"""
	def set_locked(self, locked):
		return (locked and self.lock() or self.unlock())

	""" Forward a lock request to the appropriate controller
	"""
	def forward_lock_request(self, request, game_slug, room_slug, action):

		locked = (action == 'lock')

		# Try to use our own controller
		controller = self.controller

		# Fallback to self.room controller
		if controller is None and self.room is not None:
			controller = self.room.controller

		# Fallback to self.game controller
		if controller is None and self.game is not None:
			controller = self.game.controller

		# Fallback to self.room.game controller
		if controller is None and self.room is not None:
			controller = self.room.game.controller

		# If we're the controller, proceed to lock/unlock sequence
		if controller is not None and controller.is_myself():

			print("\n#\nI am the controller, lets proceed")
			status, message = (locked and self.lock() or self.unlock())

		# Otherwise forward the request to the controller
		else:
			host, port, protocol = libraspi.get_net_info(request, controller)

			url = '%s://%s%s/%s/api/door/%s/%s/%s/' % (protocol, host, port, request.LANGUAGE_CODE, game_slug, room_slug, action)

			print("\n#\nI am *NOT* the controller, lets forward to %s" % url)
			status, message = libraspi.do_get(url)

		return status, message
