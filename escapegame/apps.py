# -*- coding: utf-8 -*-

from django.apps import AppConfig

import logging

class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)

	def taskLogger(self, pin):
		return logging.getLogger('%s.tasks.poll.gpio.%d' % (self.name, pin))
