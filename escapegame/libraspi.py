# -*- coding: utf-8 -*-

import os
import sys
import time
import requests


RUNNING_ON_PI = ' '.join(os.uname()).strip().endswith('armv7l')
if RUNNING_ON_PI:
	import RPi.GPIO as GPIO
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

def get_port_string(request, port):
	bind_port = request.is_secure() and 443 or 80
	return port != bind_port and ':%d' % port or ''

def get_net_info(request, controller):
	return (controller.hostname, get_port_string(request, controller.port), request.scheme)

#
# Notify the game websocket frontend with supplied message
#
def notify_frontend(game, message='notify'):

	from ws4redis.publisher import RedisPublisher
	from ws4redis.redis_store import RedisMessage

	if game.from_shell:
		return

	facility = 'notify-%s' % game.slug

	redis_publisher = RedisPublisher(facility=facility, broadcast=True)
	redis_publisher.publish_message(RedisMessage(message))
	print('notify_frontend("%s")' % message)


def is_valid_pin(pin):
	return pin not in invalid_pins

def is_valid_gpio(gpio):
	return gpio.pin not in invalid_pins

#
# Send signal to the supplied PIN number
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
# Get the state of the supplied PIN number
#
def get_pin(pin):

	try:
		signal = 0
		if RUNNING_ON_PI:
			GPIO.setup(pin, GPIO.IN)
			signal = GPIO.input(pin)

		state = (signal and 'HIGH' or 'LOW')
		print("Getting signal from PIN %d = %s" % (pin, state))
		return signal, 'Success'

	except Exception as err:
		return -1, 'Error: %s' % err

#
# Wait for state change on supplied PIN number until timeout expires (forever if timeout=-1)
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

#
# Cube controls
#
def cube_control(action, pin):

	try:
		if action not in [ 'lower', 'raise' ]:
			raise Exception('Invalid action `%s` in method cube_control()' % action)

		state = (action == 'raise')
		signal = (action == 'raise' and 'HIGH' or 'LOW')

		print('Sending signal %s to pin number %d' % (signal, pin))

		return set_pin(pin, state)

	except Exception as err:
		return 1, 'Error: %s' % err

#
# Door controls
#
def door_control(action, door):

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s` in method door_control()' % action)

		locked = (action == 'lock')

		# Get the controller of the door
		controller = door.raspberrypi

		if controller is None:
			controller = door.game.raspberrypi

		# Only perform physical door opening if we are the room controller.
		if controller.is_myself():
			set_pin(door.pin, locked)

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err
