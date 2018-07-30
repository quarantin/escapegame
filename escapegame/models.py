from django.db import models

#class EscapeGame(models.Model):
#	name = models.CharField(max_length=255, required=True)
#	video = models.CharField(max_length=255, required=True)
#
#class EscapeGameRoom(models.Model):
#	name = models.CharField(max_length=255, required=True)
#	door_pin = models.IntegerField(default=3, required=True)
#
#class EscapeGameChallenge(models.Model):
#	game = models.ForeinKey(EscapeGame)
#	room = models.ForeinKey(EscapeGameRoom)
#	name = models.CharField(max_length=255, required=True)
#	solved = models.BooleanField(default=False, required=True)

class EscapeGame(models.Model):
	name = models.CharField(max_length=255)
	video = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class EscapeGameRoom(models.Model):
	game = models.ForeignKey(EscapeGame, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	door_pin = models.IntegerField(default=3)
	def __str__(self):
		return '%s / %s' % (self.game, self.name)
		#return self.name


class EscapeGameChallenge(models.Model):
	room = models.ForeignKey(EscapeGameRoom, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	solved = models.BooleanField(default=False)
	def __str__(self):
		return '%s / %s / %s' % (self.room.game, self.room, self.name)
		#return self.name
