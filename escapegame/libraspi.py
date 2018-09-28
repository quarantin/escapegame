# -*- coding: utf-8 -*-

import os
import sys
import time
import requests


ARCH = ' '.join(os.uname()).strip()
RUNNING_ON_PI = ARCH.endswith('armv7l') or ARCH.endswith('armv6l')
if RUNNING_ON_PI:
	import RPi.GPIO as GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

invalid_pins = [
	1,
	2,
	3,
	4,
	5,
	6,
	8,
	9,
	14,
	17,
	20,
	25,
	27,
	28,
	30,
	34,
	39,
]

def git_version():

	try:
		import subprocess
		from siteconfig import settings
		output = subprocess.check_output([ 'git', 'rev-parse', 'HEAD' ], cwd=settings.BASE_DIR)
		return output.decode('utf-8').strip()

	except Exception as err:
		return 1, 'Error: %s' % err

def get_port_string(protocol, port):
	bind_port = (protocol is 'https' and 443 or 80)
	return port != bind_port and ':%d' % port or ''

def get_net_info(controller):
	port_string = get_port_string(controller.protocol, controller.port)
	return (controller.hostname, port_string, controller.protocol)

def do_get(url):

	try:
		import requests
		response = requests.get(url)
		return 0, 'Success', response.content

	except Exception as err:
		return 1, 'Error: %s' % err, None

#
# Send a message to the frontend on the supplied channel
#
def send_message(channel, message):
	from ws4redis.publisher import RedisPublisher
	from ws4redis.redis_store import RedisMessage

	facility = 'notify-%s' % channel
	redis_publisher = RedisPublisher(facility=facility, broadcast=True)
	redis_publisher.publish_message(RedisMessage(message))
	print('notify_frontend(channel="%s", message="%s")' % (channel, message))

#
# Notify the game websocket frontend with supplied message.
# Notify all game frontends if game is None
#
def notify_frontend(game=None, message='notify'):
	from escapegame.models import EscapeGame

	games = EscapeGame.objects.all()
	for some_game in games:

		if some_game.from_shell:
			continue

		if game is None or game == some_game:
			send_message(some_game.slug, message)

def is_valid_pin(pin):
	return pin not in invalid_pins

def is_valid_gpio(gpio):
	return gpio.pin not in invalid_pins

#
# Send signal to the supplied pin number
#
def set_pin(pin, signal):

	try:
		state = (signal and 'HIGH' or 'LOW')
		print("Sending signal %s to pin %d" % (state, pin))

		if RUNNING_ON_PI:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, signal)

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

#
# Get the state of the supplied pin number
#
def get_pin(pin):

	try:
		signal = 0
		if RUNNING_ON_PI:
			GPIO.setup(pin, GPIO.IN)
			signal = GPIO.input(pin)

		state = (signal and 'HIGH' or 'LOW')
		return 0, 'Success', signal

	except Exception as err:
		return -1, 'Error: %s' % err, None

#
# Wait for state change on supplied pin number until timeout expires (forever if timeout=-1)
#
def wait_for_pin_state_change(pin, timeout=-1):

	try:
		ret = pin
		if RUNNING_ON_PI:
			GPIO.setup(pin, GPIO.IN)
			ret = GPIO.wait_for_edge(pin, GPIO.BOTH, timeout=timeout)
			if ret is None:
				raise Exception("Timeout reached")
		else:
			secs = (timeout == -1 and sys.maxsize or timeout / 1000)
			time.sleep(secs)

		return ret, 'Success'

	except Exception as err:
		return -1, 'Error: %s' % err
