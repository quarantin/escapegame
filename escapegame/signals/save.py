# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver

from controllers.models import DoorGPIO

from escapegame.libraspi import notify_frontend


@receiver(post_save, sender=DoorGPIO)
def save_door(sender, instance, created, **kwargs):
	print('w00tw00tw00t')
	if instance.parent is not None:
		notify_frontend(instance.parent)
