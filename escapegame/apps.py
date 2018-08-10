# -*- coding: utf-8 -*-

from django.apps import AppConfig

import logging

def print_error(message):
	print('ERROR: %s' % message)

def print_info(message):
	print('INFO: %s' % message)

class EscapegameConfig(AppConfig):
	name = 'escapegame'
	#logger = logging.getLogger(name)
	logger = {
		'error': print_error,
		'info': print_info,
	}

	def taskLogger(pin):
		return logging.getLogger('%s.tasks.poll.gpio.%d' % (EscapegameConfig.name, pin))
