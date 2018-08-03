# -*- coding: utf-8 -*-

from constance import config

import os, subprocess

if config.RUNNING_ON_PI == 'True':
	import RPi.GPIO as GPIO

def is_running_on_pi():
	return ' '.join(os.uname()).strip().endswith('armv7l')

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

def set_door_locked(pin, locked):

	try:
		ret = 0
		if config.RUNNING_ON_PI == 'True':
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			ret = GPIO.output(pin, locked)

		state = (locked and 'Closing' or 'Opening')
		print("DEBUG: %s door with pin %d" % (state, pin))
		return ret, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err
