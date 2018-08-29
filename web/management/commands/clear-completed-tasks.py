from django.core.management.base import BaseCommand


import traceback

import time

import os


class Command(BaseCommand):
	help = 'Clear completed background tasks from database'

	def handle(self, *args, **options):
		from background_task.models_completed import CompletedTask
		CompletedTask.objects.all().delete()