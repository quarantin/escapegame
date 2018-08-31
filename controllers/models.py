from django.db import models

from constance import config

from escapegame import libraspi


# Controllers classes

class RaspberryPi(models.Model):

	name = models.CharField(max_length=255)
	hostname = models.CharField(max_length=32)
	port = models.IntegerField(default=80)

	def __str__(self):
		return self.name

	def is_local(self, hostname):
		return hostname == config.HOSTNAME

	def is_myself(self):
		return self.is_local(self.hostname)

	def is_master(self):
		host, port = libraspi.get_master()
		return self.is_local(host)

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
