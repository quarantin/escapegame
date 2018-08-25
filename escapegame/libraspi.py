# -*- coding: utf-8 -*-

import os, sys, subprocess, time

import socket
import traceback
import requests

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

		def __init__(self, video=None, dbus_name=DBUS_NAME):

			# Store dbus name
			self.dbus_name = dbus_name

			# If a video was supplied, start playing it now
			if video:
				from constance import config
				video_path = os.path.join(config.UPLOAD_VIDEO_PATH, video.video_path.path)
				self.play(video_path)

			# Initialize DBUS controls and properties
			self.__init_controls()

		def __init_controls(self):

			try:
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
			player.OMXPlayer(video, pause=True, dbus_name=self.dbus_name, args=[ '--no-osd' ])

		def position(self):
			return self.__basic_property('Position')

		def stop(self):
			return self.__basic_control(keys.STOP)

		def rewind(self):
			return self.__basic_control(keys.REWIND)

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

def git_version():

	try:
		from siteconfig import settings
		output = subprocess.check_output([ 'git', 'rev-parse', 'HEAD' ], cwd=settings.BASE_DIR)
		return output.decode('utf-8').strip()

	except Exception as err:
		return 1, 'Error: %s' % err

def local_video_control(action, video):

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` in method local_video_control()' % action)

		fifo = '/tmp/%s.fifo' % video.slug

		from constance import config
		video_path = os.path.join(config.UPLOAD_VIDEO_PATH, video.video_path.path)

		if action == 'pause':

			print("Pausing local video '%s'" % video_path)
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

		elif action == 'play':

			print("Playing local video '%s'" % video_path)

			if RUNNING_ON_PI:
				OMXPlayer(video)
				status = 0

			else:
				if os.path.exists(fifo):
					os.remove(fifo)

				os.mkfifo(fifo)

				from constance import config
				status = subprocess.call([ config.VIDEO_PLAYER, '--input-file', fifo, video_path ])

				os.remove(fifo)

			return status, 'Success'

		elif action == 'stop':
			print("Stopping local video '%s'" % video.video_path.url)
			if RUNNING_ON_PI:
				status, message = OMXPlayer().stop()
			else:
				from constance import config
				status, message = subprocess.call([ 'killall', config.VIDEO_PLAYER ]), 'Success'

			return status, message

	except Exception as err:
		return 1, 'Error: %s' % traceback.format_exc()

def remote_video_control(action, video):

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` in method remote_video_control()' % action)

		raspi = video.raspberrypi

		host = raspi.hostname
		port = raspi.port != 80 and ':%d' % raspi.port or ''

		url = 'http://%s%s/api/video/%s/%s/' % (host, port, video.slug, action)

		return do_get(url)

	except Exception as err:
		return 1, 'Error: %s' % traceback.format_exc()

def video_control(action, video):

	raspi = video.raspberrypi
	method = local_video_control
	if raspi:
		method = remote_video_control
		if raspi.hostname == socket.gethostname():
			method = local_video_control

	return method(action, video)

def get_pin_state(pin):

	try:
		state = 0
		if RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.IN)
			state = GPIO.input(pin)

		print("Getting pin state on pin %d = %s" % (pin, state))
		return state, 'Success'

	except Exception as err:
		return -1, 'Error: %s' % err

def set_door_locked(pin, locked):

	try:
		state = not locked
		if RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, state)

		state = (state and 'Opening' or 'Closing')
		print("%s door on pin %d" % (state, pin))
		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def set_led_status(pin, onoff):

	try:
		state = not onoff
		if RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, state)

		state = (state and 'on' or 'off')
		print("Turning %s led on pin %d" % (state, pin))
		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

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
