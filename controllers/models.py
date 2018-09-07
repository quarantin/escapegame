# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from constance import config

from escapegame import libraspi

import os


# Controllers classes

class ArduinoSketch(models.Model):

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

	class Meta:
		verbose_name = 'Arduino Sketch'
		verbose_name_plural = 'Arduino Sketches'

class RaspberryPi(models.Model):

	name = models.CharField(max_length=255, unique=True)
	hostname = models.CharField(max_length=255, unique=True)
	port = models.IntegerField(default=80)

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
		return RaspberryPi.get_by_name(config.HOSTNAME)

	def is_myself(self, hostname=config.HOSTNAME):
		return hostname == self.hostname

	class Meta:
		verbose_name = 'Raspberry Pi'
		verbose_name_plural = 'Raspberry Pis'

class GPIO(models.Model):

	slug = models.SlugField(max_length=255, unique=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	raspberrypi = models.ForeignKey(RaspberryPi, null=True, on_delete=models.CASCADE)
	pin = models.IntegerField(default=7)

	def __str__(self):
		return 'GPIO - %s' % self.name

	def clean(self):
		if not libraspi.is_valid_pin(self.pin):
			raise ValidationError({
				'pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % self.pin,
			})

	def save(self, *args, **kwargs):
		new_slug = slugify(self.name)
		if self.slug is None or self.slug != new_slug:
			self.slug = new_slug

		self.clean()
		super(GPIO, self).save(*args, **kwargs)

	""" Read value from this GPIO
	"""
	def read(self):
		return libraspi.get_pin(self.pin)

	""" Write value to this GPIO
	"""
	def write(self, signal):
		return libraspi.set_pin(self.pin, signal)

	class Meta:
		verbose_name = 'GPIO'
		verbose_name_plural = 'GPIOs'

class Challenge(GPIO):

	solved = models.BooleanField(default=False)
	solved_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return 'Challenge GPIO - %s' % self.name

	def save(self, *args, **kwargs):
		self.clean()
		super(Challenge, self).save(*args, **kwargs)

	""" Reset this challenge state
	"""
	def reset(self):
		self.solved = False
		self.solved_at = None
		self.save()
		return 0, 'Success'

	""" Callback method to call when this challenge has just been solved
	"""
	def solve(self):
		self.solved = True
		if self.solved_at is None:
			self.solved_at = timezone.localtime()

		self.save()
		return 0, 'Success'

class Cube(GPIO):

	tag_id = models.CharField(max_length=32)
	taken_at = models.DateTimeField(blank=True, null=True)
	placed_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return 'Cube - %s' % self.name

	def save(self, *args, **kwargs):
		self.clean()
		super(Cube, self).save(*args, **kwargs)

	""" Reset this cube state
	"""
	def reset(self):
		self.taken_at = None
		self.placed_at = None
		self.save()
		return self.lowerStand()

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

class Door(GPIO):

	locked = models.BooleanField(default=True)
	unlocked_at = models.DateTimeField(blank=True, null=True)
	game = models.ForeignKey('escapegame.EscapeGame', null=True, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return 'Door - %s' % self.name

	def save(self, *args, **kwargs):
		self.clean()
		super(Door, self).save(*args, **kwargs)

	""" Reset this door state
	"""
	def reset(self):
		self.unlocked_at = None

		return self.lock()

	""" Lock this door
	"""
	def lock(self):
		self.locked = True

		print("Locking door `%s`" % self.name)
		status, message = libraspi.door_control('lock', self)
		if status != 0:
			raise Exception('Failed locking door `%s`' % self.name)

		self.save()
		return status, message

	""" Unlock this door
	"""
	def unlock(self):
		self.locked = False

		if self.unlocked_at is None:
			self.unlocked_at = timezone.localtime()

		print("Unlocking door `%s`" % self.name)
		status, message = libraspi.door_control('unlock', self)
		if status != 0:
			raise Exception('Failed unlocking door `%s`' % self.name)

		self.save()
		return status, message

	""" Set the state of this door lock
	"""
	def set_locked(self, locked):
		return (locked and self.lock() or self.unlock())
