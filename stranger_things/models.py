from django.db import models

default_duration_door = 10
default_duration_led = 10

class StrangerThingsSettings(models.Model):

	# Dark door (Sombre)
	pin_door_dark = models.IntegerField()
	pin_door_dark_duration = models.IntegerField(default=default_duration_door)

	# Light door (Claire)
	pin_door_cave = models.IntegerField()
	pin_door_cave_duration = models.IntegerField(default=default_duration_door)

	# Wood door (Bois)
	pin_door_wood = models.IntegerField()
	pin_door_wood_duration = models.IntegerField(default=default_duration_door)

	# Cabin door (Cabane)
	pin_door_cabin = models.IntegerField()
	pin_door_cabin_duration = models.IntegerField(default=default_duration_door)

	# TODO LED PINs...
	# pin_led_whatever = models.IntegerField()
	# pin_led_whatever_duration = models.IntegerField(default=default_duration_led)
