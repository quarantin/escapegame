# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = 'Clear completed background tasks from database'

	def handle(self, *args, **options):
		try:
			from background_task.models_completed import CompletedTask
			CompletedTask.objects.all().delete()
		except CompletedTask.DoesNotExist:
			pass
