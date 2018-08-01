from django.db import models
from django.template.defaultfilters import slugify

class EscapeGame(models.Model):

	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, editable=False)
	video_path = models.CharField(max_length=255)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(EscapeGame, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class EscapeGameRoom(models.Model):

	name = models.CharField(max_length=255)
	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	door_pin = models.IntegerField(default=3)

	def __str__(self):
		return '%s / %s' % (self.game, self.name)

class EscapeGameChallenge(models.Model):

	name = models.CharField(max_length=255)
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)
	solved = models.BooleanField(default=False)

	def __str__(self):
		return '%s / %s' % (self.room, self.name)
