# -*- coding: utf-8 -*-

from django.db import models
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
