# -*- coding: utf-8 -*-

from django.apps import apps
from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):
	help = 'Show table names for all models registered to this site'


	def handle(self, *args, **options):

		app_list = [
			'escapegame',
			'controllers',
			'multimedia',
		]

		for app in app_list:
			models = apps.get_app_config(app).get_models()
			for model in models:
				print(model._meta.db_table)
