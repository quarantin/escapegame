from django.utils import timezone

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from escapegame.models import *

from datetime import datetime

import time

import os

delay = os.getenv('WEBSOCKET_DELAY') or 1

redis_publisher = RedisPublisher(facility='notify', broadcast=True)

while True:

	game = EscapeGame.objects.get(pk=1)

	before = game.start_time
	if before:
		now = timezone.localtime()
		message = ('%s' % (now - before)).split('.')[0]
		print("Sending `%s`" % message)
		redis_publisher.publish_message(RedisMessage(message))

	redis_publisher.publish_message(RedisMessage('notify'))
	time.sleep(delay)
