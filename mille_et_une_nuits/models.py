from django.db import models

default_duration_door = 10
default_duration_led = 10

class MilleEtUneNuitsSettings(models.Model):

	# Garden door (Jardin)
	pin_door_garden = models.IntegerField()
	pin_door_garden_duration = models.IntegerField(default=default_duration_door)

	# Cave door (Caverne)
	pin_door_cave = models.IntegerField()
	pin_door_cave_duration = models.IntegerField(default=default_duration_door)

	# Lamp door (Lampe)
	pin_door_lamp = models.IntegerField()
	pin_door_lamp_duration = models.IntegerField(default=default_duration_door)

	# TODO LED PINs...
	# pin_led_whatever = models.IntegerField()
	# pin_led_whatever_duration = models.IntegerField(default=default_duration_led)
