# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import timezone

from escapegame.models import EscapeGame, EscapeGameRoom
from escapegame import libraspi

import os
import time
import traceback


class Command(BaseCommand):
	help = 'Websocket timer process to notify web frontend for all escape games'

	def publish_reset(self, game):

		libraspi.notify_frontend(game, '0:00:00')

	def publish_counter(self, game, start_time, finish_time=None):

		if not finish_time:
			finish_time = timezone.localtime()

		message = ('%s' % (finish_time - start_time)).split('.')[0]

		libraspi.notify_frontend(game, message)

	def get_start_time(self, sas_rooms):

		for room in sas_rooms:
			if room.door.unlocked_at is None:
				return None

		max_room = max(sas_rooms, key=lambda x: x.door.unlocked_at)

		return max_room.door.unlocked_at

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting websocket timer process'))

		delay = os.getenv('WEBSOCKET_DELAY') or 1

		game_started = {}

		while True:

			try:
				games = EscapeGame.objects.all()

				for game in games:

					sas_rooms = EscapeGameRoom.objects.filter(game=game, is_sas=True)

					start_time = self.get_start_time(sas_rooms)

					if game not in game_started:
						game_started[game] = True

					if start_time and game.finish_time:
						game_started[game] = False
						self.publish_counter(game, start_time, game.finish_time)

					elif start_time:
						game_started[game] = True
						self.publish_counter(game, start_time)

					elif game_started[game]:
						game_started[game] = False
						self.publish_reset(game)

					else:
						self.stdout.write('  No message to send [facility=notify-%s]' % game.slug)
			except:
				self.stdout.write(traceback.format_exc())

			time.sleep(delay)
