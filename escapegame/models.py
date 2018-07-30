from django.db import models

class EscapeGame(models.Model):

	name = models.CharField(max_length=255)
	video_path = models.CharField(max_length=255)

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
