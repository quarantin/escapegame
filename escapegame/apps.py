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

		# Register video player task
		# (Only if the table exists to avoid errors when populating database)
		#from multimedia import tasks
		#from django.db import connection
		#db_tables = connection.introspection.table_names()
		#if 'multimedia_video' in db_tables:
		#	tasks.setup_background_tasks()
