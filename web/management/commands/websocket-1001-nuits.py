from django.core.management.base import BaseCommand
from django.utils import timezone

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from escapegame.models import *

import traceback

import time

import os


class Command(BaseCommand):
	help = 'Websocket process for escape game `Les 1001 nuits`'

	def send_message(self, message):
		self.stdout.write('Sending `%s`' % message, ending='')
		redis_publisher = RedisPublisher(facility='notify', broadcast=True)
		redis_publisher.publish_message(RedisMessage(message))

	def reset_counter(self):
		self.send_message('0:00:00')

	def publish_counter(self, start_time):
		now = timezone.localtime()
		message = ('%s' % (now - start_time)).split('.')[0]
		self.send_message(message)

	def handle(self, *args, **options):

		self.stdout.write('WTFFFFF', ending='')
		delay = os.getenv('WEBSOCKET_DELAY') or 1

		started = True
		while True:

			try:
				game = EscapeGame.objects.all().order_by('id').first()
				room = EscapeGameRoom.objects.filter(escapegame=game).order_by('id').first()

				start_time = room.start_time

				if start_time:
					started = True
					self.publish_counter(start_time)

				elif started:
					started = False
					self.reset_counter()

				else:
					self.stdout.write('No message to send', ending='')

			except:
				self.stdout.write(traceback.format_exc(), ending='')

			time.sleep(delay)
