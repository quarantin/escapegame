from django.db import models
from constance import config

from jsonexport.decorators import json_import

# Controllers classes

@json_import
class RaspberryPi(models.Model):

	name = models.CharField(max_length=255)
	hostname = models.CharField(max_length=32)
	port = models.IntegerField(default=8000)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Raspberry Pi'
		verbose_name_plural = 'Raspberry Pis'

@json_import
class RemoteChallengePin(models.Model):
	
	name = models.CharField(max_length=255)
	challenge = models.ForeignKey('escapegame.EscapeGameChallenge', on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	url_callback_validate = models.URLField(max_length=255)
	url_callback_reset = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def save(self, **kwargs):

		host = config.MASTER_HOSTNAME
		port = (config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or '')
		game_slug = self.challenge.room.escapegame.slug
		room_slug = self.challenge.room.slug
		chall_slug = self.challenge.slug

		self.url_callback_validate = 'http://%s%s/web/%s/%s/%s/validate/' % (host, port, game_slug, room_slug, chall_slug)
		self.url_callback_reset = 'http://%s%s/web/%s/%s/%s/reset/' % (host, port, game_slug, room_slug, chall_slug)

		super(RemoteChallengePin, self).save(**kwargs)

@json_import
class RemoteDoorPin(models.Model):

	name = models.CharField(max_length=255)
	room = models.ForeignKey('escapegame.EscapeGameRoom', on_delete=models.CASCADE)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	url_callback_lock = models.URLField(max_length=255)
	url_callback_unlock = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def save(self, **kwargs):

		host = config.MASTER_HOSTNAME
		port = (config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or '')
		game_slug = self.room.escapegame.slug
		room_slug = self.room.slug

		self.url_callback_lock = 'http://%s%s/web/%s/%s/lock/' % (host, port, game_slug, room_slug)
		self.url_callback_unlock = 'http://%s%s/web/%s/%s/unlock/' % (host, port, game_slug, room_slug)

		super(RemoteDoorPin, self).save(**kwargs)

@json_import
class RemoteLedPin(models.Model):

	name = models.CharField(max_length=255)
	raspberrypi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
	pin_number = models.IntegerField(default=7)
	url_on = models.URLField(max_length=255)
	url_off = models.URLField(max_length=255)

	def __str__(self):
		return self.name

	def save(self, **kwargs):

		host = self.raspberrypi.hostname
		port = (self.raspberrypi.port != 80 and ':%d' % self.raspberrypi.port or '')

		self.url_on = 'http://%s%s/api/led/on/%d/' % (host, port, self.pin_number)
		self.url_off = 'http://%s%s/api/led/off/%d/' % (host, port, self.pin_number)

		super(RemoteLedPin, self).save(**kwargs)

	class Meta:
		verbose_name = 'Remote LED pin'
		verbose_name_plural = 'Remote LED pins'
