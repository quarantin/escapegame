from django.utils import timezone

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

import time

import os

delay = os.getenv('WEBSOCKET_DELAY') or 1

redis_publisher = RedisPublisher(facility='w00t', broadcast=True)

while True:

	datestr = '%s' % timezone.localtime()

	print("Sending %s" % datestr)

	message = RedisMessage(datestr)

	redis_publisher.publish_message(message)

	time.sleep(delay)
