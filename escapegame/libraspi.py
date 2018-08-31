# -*- coding: utf-8 -*-

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

import os
import sys
import time
import getpass
import requests
import traceback
import subprocess


RUNNING_ON_PI = ' '.join(os.uname()).strip().endswith('armv7l')
if RUNNING_ON_PI:
	import RPi.GPIO as GPIO
	from omxplayer import keys, player
	from omxplayer.bus_finder import BusFinder
	import dbus

	DBUS_NAME = 'org.mpris.MediaPlayer2.omxplayer'

	class OMXPlayer:

		dbus_name = None
		controls = None
		properties = None

		def __init__(self, video_path=None, dbus_name=DBUS_NAME):

			# Store dbus name
			self.dbus_name = dbus_name

			# If a video was supplied, start playing it now
			if video_path:
				self.play(video_path)

			# Initialize DBUS controls and properties
			self.__init_controls()

		def __init_controls(self):

			try:
				socket_path = '/tmp/omxplayerdbus.%s' % getpass.getuser()
				if not os.path.exists(socket_path):
					socket_path = '/tmp/omxplayerdbus.root'
					if not os.path.exists(socket_path):
						return

				# Get the bus connection of omxplayer
				bus = dbus.bus.BusConnection(BusFinder().get_address())

				# Retrieve omxplayer dbus handle
				handle = bus.get_object(self.dbus_name, '/org/mpris/MediaPlayer2', introspect=False)

				# Retrieve omxplayer controls and properties through dbus handle
				self.controls = dbus.Interface(handle, 'org.mpris.MediaPlayer2.Player')
				self.properties = dbus.Interface(handle, 'org.freedesktop.DBus.Properties')

			except Exception as err:
				pass

		def __basic_control(self, key):

			try:
				if not self.controls:

					self.__init_controls()
					if not self.controls:
						return 1, 'No video running'

				self.controls.Action(key)
				return 0, 'Success'

			except Exception as err:
				print('Error: %s' % err)
				return 1, str(err)

		def __basic_property(self, key):

			try:
				if not self.properties:

					self.__init_controls()
					if not self.properties:
						return

				return self.properties.Get(key)

			except Exception as err:
				print('Error: %s' % err)

		def duration(self):
			return self.__basic_property('Duration')

		def fast_forward(self):
			return self.__basic_control(keys.FAST_FORWARD)

		def pause(self):
			return self.__basic_control(keys.PAUSE)

		def play(self, video):
			player.OMXPlayer(video, pause=False, dbus_name=self.dbus_name, args=[ '--no-osd' ])

		def position(self):
			return self.__basic_property('Position')

		def stop(self):
			return self.__basic_control(keys.EXIT)

		def rewind(self):
			return self.__basic_control(keys.REWIND)


def git_version():

	try:
		from siteconfig import settings
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

	facility = 'notify-%s' % game.slug

	redis_publisher = RedisPublisher(facility=facility, broadcast=True)
	redis_publisher.publish_message(RedisMessage(message))
	print('notify_frontend("%s")' % message)

#
# Video controls:
#
#   - __local_video_control_pause
#   - __local_video_control_play
#   - __local_video_control_stop
#   - __local_video_control
#   - __remote_video_control
#   - video_control

def __local_video_control_pause(fifo):

	if RUNNING_ON_PI:
		status, message = OMXPlayer().pause()

	else:
		status, message = 1, 'Fifo %s could not be found' % fifo
		if os.path.exists(fifo):
			fout = open(fifo, 'w')
			fout.write('pause\n')
			fout.close()
			status, message = 0, 'Success'

	return status, message

def __local_video_control_play(fifo, video_path):

	if RUNNING_ON_PI:
		OMXPlayer(video_path)
		status = 0

	else:
		if os.path.exists(fifo):
			os.remove(fifo)

		os.mkfifo(fifo)

		from constance import config
		status = subprocess.call([ config.VIDEO_PLAYER, '--input-file', fifo, video_path ])

		os.remove(fifo)

	return status, 'Success'

def __local_video_control_stop():

	if RUNNING_ON_PI:
		status, message = OMXPlayer().stop()

	else:
		from constance import config
		status, message = subprocess.call([ 'killall', config.VIDEO_PLAYER ]), 'Success'

	return status, message

def video_control(action, video):

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` in method video_control()' % action)

		fifo = '/tmp/%s.fifo' % video.slug

		host, port = get_master()

		video_url = 'http://%s%s/media%s' % (host, port, video.video_path.url)
		print("DEBUG WTF: Video URL: %s" % video_url)

		if action == 'pause':
			print("Pausing video '%s'" % video.video_name)
			return __local_video_control_pause(fifo)

		elif action == 'play':
			print("Playing video '%s'" % video.video_name)
			return __local_video_control_play(fifo, video_path)

		elif action == 'stop':
			print("Stopping video '%s'" % video.video_path.url)
			return __local_video_control_stop()

	except Exception as err:
		return 1, 'Error: %s' % traceback.format_exc()

#
# Door controls:
#
#   - door_control
#

def door_control(action, room, pin):

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s` in method door_control()' % action)

		locked = (action != 'lock')

		host, port = get_master()

		# Get the controller of the room
		controller = room and room.get_controller()

		# If the room has no controllers, it means we're running on the master
		if not controller:

			# So we create the callback URL to notify web frontend
			url = 'http://%s%s/web/%s/%s/%s/' % (host, port, room.escapegame.slug, room.slug, action)

			# TODO fix URL to call API then call new URL then notify frontend

		# Otherwise we're running on a slave
		else:

			# Only perform physical door opening if we are the room controller.
			# Since we are a dedicated escape game controller, callback to master.
			if controller.is_myself():
				if RUNNING_ON_PI:
					GPIO.setmode(GPIO.BOARD)
					GPIO.setup(pin, GPIO.OUT)
					GPIO.output(pin, locked)

			# Otherwise we want to notify the change to the room controller which
			# will be responsible for propagating the change to the master.
			else:
				host, port = get_net_info(controller.hostname, controller.port)

			# Create the callback URL to notify next controller backend
			url = 'http://%s%s/api/door/%s/%d/' % (host, port, action, pin)

		action = (locked and 'Opening' or 'Closing')
		print("%s door on PIN %d" % (action, pin))

		# Perform call to callback URL to inform next controller
		return do_get(url)

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
