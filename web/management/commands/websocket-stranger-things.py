from django.core.management.base import BaseCommand
from django.utils import timezone

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from escapegame.models import *

import traceback

import time

import os


class Command(BaseCommand):
	help = 'Websocket process for escape game `Stranger Things`'

	def get_game(self):
		return EscapeGame.objects.all().order_by('id').last()

	def get_trigger_rooms(self, game):
		rooms = EscapeGameRoom.objects.filter(escapegame=game).order_by('id')
		room1 = rooms[0]
		room2 = rooms[1]
		return room1, room2

	def send_message(self, message):
		game = self.get_game()
		self.stdout.write('  Sending %s' % message)
		redis_publisher = RedisPublisher(facility='notify-%s' % game.escapegame_name, broadcast=True)
		redis_publisher.publish_message(RedisMessage(message))

	def reset_counter(self):
		self.send_message('0:00:00')

	def publish_counter(self, start_time):
		now = timezone.localtime()
		message = ('%s' % (now - start_time)).split('.')[0]
		self.send_message(message)


	def handle(self, *args, **options):

		game = self.get_game()
		self.stdout.write(self.style.MIGRATE_HEADING('Starting websocket for `%s`' % game.escapegame_name))
		delay = os.getenv('WEBSOCKET_DELAY') or 1

		started = True
		while True:

			try:
				game = self.get_game()
				room1, room2 = self.get_trigger_rooms(game)

				start_time = None
				if room1.start_time and room2.start_time:
					start_time = max(room1.start_time, room2.start_time)

				if start_time:
					started = True
					self.publish_counter(start_time)

				elif started:
					started = False
					self.reset_counter()

				else:
					self.stdout.write('  No message to send')

			except:
				self.stdout.write(traceback.format_exc())

			time.sleep(delay)
