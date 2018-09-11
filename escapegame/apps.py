# -*- coding: utf-8 -*-

from django.db import connection
from django.apps import AppConfig

import logging


class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)

	def ready(self):
		from multimedia import tasks as ext_tasks
		from . import tasks as int_tasks
		from .signals import save
		from .signals import constance

		db_tables = connection.introspection.table_names()

		if 'escapegame_escapegame' in db_tables:
		   int_tasks.setup_background_tasks()

		if 'multimedia_video' in db_tables:
			ext_tasks.setup_background_tasks()

	def taskLogger(pin):
		return logging.getLogger('%s.tasks.poll.gpio.%d' % (EscapegameConfig.name, pin))
