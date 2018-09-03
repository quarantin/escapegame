# -*- coding: utf-8 -*-

from django.db import connection
from django.apps import AppConfig

import logging


class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)

	def ready(self):
		from . import tasks
		from .signals import constance

		db_tables = connection.introspection.table_names()
		if 'escapegame_escapegame' in db_tables:
		   tasks.setup_background_tasks()

	def taskLogger(pin):
		return logging.getLogger('%s.tasks.poll.gpio.%d' % (EscapegameConfig.name, pin))
