from django.db import models

class VideoPlayer(models.Model):

	video_player = models.CharField(max_length=255)

	def __str__(self):
		return self.video_player
