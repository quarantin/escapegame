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
		return self.name

	def get_myself():
		try:
			return RaspberryPi.objects.get(hostname=config.HOSTNAME)
		except RaspberryPi.DoesNotExist:
			return None

	def is_myself(self, hostname=config.HOSTNAME):
		return hostname == self.hostname

	def is_master(self):
		host, port = libraspi.get_master()
		return self.is_myself(host)

	class Meta:
		verbose_name = 'Raspberry Pi'
		verbose_name_plural = 'Raspberry Pis'

class RemoteChallengePin(models.Model):

	name = models.CharField(max_length=255)
	challenge = models.ForeignKey('escapegame.EscapeGameChallenge', on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	url_callback_validate = models.URLField(max_length=255)
	url_callback_reset = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def save(self, **kwargs):

		host, port = libraspi.get_master()

		game_slug = self.challenge.room.escapegame.slug
		room_slug = self.challenge.room.slug
		chall_slug = self.challenge.slug

		self.url_callback_validate = 'http://%s%s/web/%s/%s/%s/validate/' % (host, port, game_slug, room_slug, chall_slug)
		self.url_callback_reset = 'http://%s%s/web/%s/%s/%s/reset/' % (host, port, game_slug, room_slug, chall_slug)

		super(RemoteChallengePin, self).save(**kwargs)

class RemoteDoorPin(models.Model):

	name = models.CharField(max_length=255)
	room = models.ForeignKey('escapegame.EscapeGameRoom', on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	url_callback_lock = models.URLField(max_length=255)
	url_callback_unlock = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def save(self, **kwargs):

		host, port = libraspi.get_master()

		game_slug = self.room.escapegame.slug
		room_slug = self.room.slug

		self.url_callback_lock = 'http://%s%s/web/%s/%s/lock/' % (host, port, game_slug, room_slug)
		self.url_callback_unlock = 'http://%s%s/web/%s/%s/unlock/' % (host, port, game_slug, room_slug)

		super(RemoteDoorPin, self).save(**kwargs)
