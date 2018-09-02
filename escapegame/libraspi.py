# -*- coding: utf-8 -*-

import os
import sys
import time
import requests


RUNNING_ON_PI = ' '.join(os.uname()).strip().endswith('armv7l')
if RUNNING_ON_PI:
	import RPi.GPIO as GPIO


def git_version():

	try:
		import subprocess
		import siteconfig.settings
		output = subprocess.check_output([ 'git', 'rev-parse', 'HEAD' ], cwd=settings.BASE_DIR)
		return output.decode('utf-8').strip()

	except Exception as err:
		return 1, 'Error: %s' % err


def get_port_string(port):

	return port != 80 and ':%d' % port or ''


def get_net_info(host, port):

	return (host, get_port_string(port))


def get_master():

	from constance import config

	return get_net_info(config.MASTER_HOSTNAME, config.MASTER_PORT)

#
# Web
#
#   - do_get
#   - do_post
#   - notify_frontend
#

def do_get(url):
	try:
		print('libraspi.do_get(url=%s)' % url)
		response = requests.get(url)
		if not response:
			raise Exception("requests.get(url=%s) failed!" % url)

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def do_post(url, data):
	try:
		print("Performing request POST %s data=%s" % (url, data))
		response = request.post(url, data=data)
		if not response:
			raise Exception("requests.port(url=%s, data=%s) failed!" % (url, data))

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def notify_frontend(game, message='notify'):

	from ws4redis.publisher import RedisPublisher
	from ws4redis.redis_store import RedisMessage

	facility = 'notify-%s' % game.slug

	redis_publisher = RedisPublisher(facility=facility, broadcast=True)
	redis_publisher.publish_message(RedisMessage(message))
	print('notify_frontend("%s")' % message)

#
# Door controls:
#
#   - door_control
#

def door_control(action, room):

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s` in method door_control()' % action)

		locked = (action == 'lock')

		# Get the controller of the room
		controller = room.get_controller()

		# Only perform physical door opening if we are the room controller.
		if controller.is_myself():
			if RUNNING_ON_PI:
				GPIO.setmode(GPIO.BOARD)
				GPIO.setup(room.door_pin, GPIO.OUT)
				GPIO.output(room.door_pin, locked)

		action = (locked and 'Opening' or 'Closing')
		print("%s door on PIN %d" % (action, room.door_pin))

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

#
# Challenge controls
#   - challenge_control
#
#

def challenge_control(action, challenge):

	try:
		if action not in [ 'validate', 'reset' ]:
			raise Exception('Invalid action `%s` in method challenge_control()' % action)

		solved = (action == 'validate')

		controller = challenge.get_controller()

		if not controller:

			host, port = get_master()

			url = 'http://%s%s/web/%s/%s/%s/' % (host, port, challenge.room.escapegame.slug, challenge.room.slug, challenge.slug)

			# TODO

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

#
# Cube controls
#   - cube_control
#

def cube_control(action, pin):

	try:
		if action not in [ 'lower', 'raise' ]:
			raise Exception('Invalid action `%s` in method cube_control()' % action)

		state = (action == 'raise')
		signal = (action == 'raise' and 'HIGH' or 'LOW')

		print('Sending signal %s to pin number %d' % (signal, pin))

		return set_pin_state(pin, state)

	except Exception as err:
		return 1, 'Error: %s' % err

#
# PINs and LEDs controls
#   - is_valid_pin
#   - set_led_status
#   - get_pin_state
#   - wait_for_pin_state_change
#

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

def is_valid_pin(pin):
	return pin not in invalid_pins

def set_pin_state(pin, state):

	try:
		#signal = (state and 'HIGH' or 'LOW')
		#print("Sending signal %s to pin %d" % (signal, pin))

		if RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, state)

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def get_pin_state(pin):

	try:
		state = 0
		if RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.IN)
			state = GPIO.input(pin)

		print("Getting pin state on PIN %d = %s" % (pin, state))
		return state, 'Success'

	except Exception as err:
		return -1, 'Error: %s' % err

def wait_for_pin_state_change(pin, timeout=-1):

	try:
		ret = pin
		if RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
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
