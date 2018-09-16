# -*- coding: utf-8 -*-

from django.apps import AppConfig

import logging


class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)

	def ready(self):

		# Register signals
		from .signals import save
		from .signals import constance
