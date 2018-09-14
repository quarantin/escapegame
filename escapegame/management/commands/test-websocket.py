# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import timezone

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from ws4redis.exceptions import WebSocketError

from escapegame.models import EscapeGame, EscapeGameRoom

import os
import time
import traceback


class Command(BaseCommand):
	help = 'Websocket timer process to notify web frontend for all escape games'

	def send_message(self, game, message):

		facility = 'notify-%s' % game.slug
		self.stdout.write('  Sending %s [facility=%s]' % (message, facility))

		redis_publisher = RedisPublisher(facility=facility, broadcast=True)
		redis_publisher.publish_message(RedisMessage(message))

	def handle(self, *args, **options):

		self.stdout.write(self.style.MIGRATE_HEADING('Starting websocket timer process'))

		delay = os.getenv('WEBSOCKET_DELAY') or 1

		while True:

			try:
				games = EscapeGame.objects.all()

				for game in games:
					self.send_message(game, 'notify')

			except:
				self.stdout.write(traceback.format_exc())

			time.sleep(delay)
