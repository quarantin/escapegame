# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from escapegame.models import *
from multimedia.models import *
from controllers.models import *


class Command(BaseCommand):

	def flush_database(self):

		all_models = [
			Image,
			MultimediaFile,
			RaspberryPi,   # RaspberryPi before Controller (parent model)
			Controller,
			ChallengeGPIO, # ChallengeGPIO before GPIO (parent model)
			DoorGPIO,      # DoorGPIO before GPIO (parent model)
			LiftGPIO,      # LiftGPIO before GPIO (parent model)
			GPIO,
			EscapeGameChallenge,
			EscapeGameRoom,
			EscapeGameCube,
			EscapeGame,
		]

		self.stdout.write(self.style.MIGRATE_HEADING('Flushing database:'))

		for model in all_models:

			self.stdout.write('  Flushing model `%s`' % model.__name__, ending='')

			try:
				model.objects.all().delete()
				self.stdout.write(self.style.SUCCESS(' OK'))
			except:
				self.stdout.write(self.style.SUCCESS(' MISSING'))

	def handle(self, *args, **options):

		EscapeGame.from_shell = True

		# We want to clear the database before populating it to avoid duplicate entries.
		self.flush_database()
