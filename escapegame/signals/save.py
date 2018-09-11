# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver

from controllers.models import ChallengeGPIO, CubeGPIO, DoorGPIO
from escapegame.libraspi import notify_frontend


@receiver(post_save, sender=ChallengeGPIO)
def save_challenge_gpio(sender, instance, created, **kwargs):
	if instance.challenge is not None:
		notify_frontend(instance.challenge.room.game)

@receiver(post_save, sender=CubeGPIO)
def save_cube_gpio(sender, instance, created, **kwargs):
	if instance.challenge is not None:
		notify_frontend(instance.challenge.room.game)

@receiver(post_save, sender=DoorGPIO)
def save_door_gpio(sender, instance, created, **kwargs):
	if instance.game is not None:
		notify_frontend(instance.game)
