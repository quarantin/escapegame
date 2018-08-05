# -*- coding: utf-8 -*-

from constance import config

import os, subprocess
import requests

if config.RUNNING_ON_PI:
	import RPi.GPIO as GPIO

def is_running_on_pi():
	return ' '.join(os.uname()).strip().endswith('armv7l')

def do_get(url):
	try:
		# Why the fuck is this not working???
		#response = requests.get(url)
		#if not response:
		#	return None
		#
		#return 0, response.content

		print("Performing request GET %s" % url)
		os.system('wget -q -O /dev/null %s' % url)

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def do_post(url, data):
	try:
		print("Performing request POST %s data=%s" % (url, data))
		response = request.post(url, data=data)
		if not response:
			return None

		return 0, response.content

	except Exception as err:
		return 1, 'Error: %s' % err

def play_video(video_path):

	try:
		video_path = os.path.join(config.VIDEO_PATH, video_path)

		print("DEBUG: Playing video '%s'" % video_path)
		return subprocess.call([ config.VIDEO_PLAYER, video_path ]), 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def stop_video(video_path):

	try:
		print("DEBUG: Stopping video '%s'" % video_path)
		return subprocess.call([ 'killall', config.VIDEO_PLAYER ]), 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def get_pin_state(pin):

	try:
		ret = 0
		if config.RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.IN)
			ret = GPIO.output(pin, state)

		print("DEBUG: Getting pin state on pin %d = %s" % (pin, ret))
		return ret, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def set_door_locked(pin, locked):

	try:
		state = not locked
		if config.RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, state)

		state = (state and 'Opening' or 'Closing')
		print("DEBUG: %s door on pin %d" % (state, pin))
		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def set_led_status(pin, onoff):

	try:
		state = not onoff
		if config.RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, state)

		state = (state and 'on' or 'off')
		print("DEBUG: Turning %s led on pin %d" % (state, pin))
		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err
