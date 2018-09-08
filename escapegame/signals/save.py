# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver

from controllers.models import Door

from escapegame.libraspi import notify_frontend


@receiver(post_save, sender=Door)
def save_door(sender, instance, created, **kwargs):
	print('w00tw00tw00t')
	if instance.game is not None:
		notify_frontend(instance.game)
