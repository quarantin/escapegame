# -*- coding: utf-8 -*-

from django.apps import AppConfig

import logging

class MyLogger:
	def error(message):
		print('ERROR: %s' % message)

	def info(message):
		print('INFO: %s' % message)

class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)
	#logger = MyLogger()

	def taskLogger(pin):
		return logging.getLogger('%s.tasks.poll.gpio.%d' % (EscapegameConfig.name, pin))
