from django.db import models
from escapegame.models import SingletonModel

invalid_pin = -1
default_duration_door = 10
default_duration_led = 10
default_video_path = '/opt/vc/src/hello_pi/hello_video/test.h264'
default_video_player = 'omxplayer'

class MilleEtUneNuitsSettings(SingletonModel):

	# Path to welcome video
	video_path = models.CharField(max_length=255, default=default_video_path)

	# Video player name
	video_player = models.CharField(max_length=255, default=default_video_player)

	# Garden door (Jardin)
	pin_door_garden = models.IntegerField(default=invalid_pin)
	pin_door_garden_duration = models.IntegerField(default=default_duration_door)

	# Cave door (Caverne)
	pin_door_cave = models.IntegerField(default=invalid_pin)
	pin_door_cave_duration = models.IntegerField(default=default_duration_door)

	# Lamp door (Lampe)
	pin_door_lamp = models.IntegerField(default=invalid_pin)
	pin_door_lamp_duration = models.IntegerField(default=default_duration_door)

	# TODO LED PINs...
	# pin_led_whatever = models.IntegerField(default=invalid_pin)
	# pin_led_whatever_duration = models.IntegerField(default=default_duration_led)
