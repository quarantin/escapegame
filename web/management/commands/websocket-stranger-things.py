from django.utils import timezone
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from escapegame.models import *

import traceback

import time

import os


delay = os.getenv('WEBSOCKET_DELAY') or 1

def send_message(message):
	print('Sending `%s`' % message)
	redis_publisher = RedisPublisher(facility='notify', broadcast=True)
	redis_publisher.publish_message(RedisMessage(message))

def reset_counter():
	send_message('0:00:00')

def publish_counter(start_time):
	now = timezone.localtime()
	message = ('%s' % (now - start_time)).split('.')[0]
	send_message(message)

started = True
while True:

	try:
		game = EscapeGame.objects.get(slug='stranger-things')
		rooms = EscapeGameRoom.objects.filter(escapegame=game).order_by('id')[0:2]

		start_time = None
		if rooms[0].start_time and rooms[1].start_time:
			start_time = max(rooms[0].start_time, rooms[1].start_time)

		if start_time:
			started = True
			publish_counter(start_time)

		elif started:
			started = False
			reset_counter()

		else:
			print('No message to send')

	except:
		print(traceback.format_exc())

	time.sleep(delay)
