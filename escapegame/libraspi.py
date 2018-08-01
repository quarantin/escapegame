# -*- coding: utf-8 -*-

from django_admin_conf_vars.global_vars import config

import os, subprocess

try:
	import RPi.GPIO as GPIO
except:
	pass

def play_video(video_path):

	try:

		video_path = os.path.join(config.VIDEO_PATH, video_path)

		print("DEBUG: Playing video '%s'" % video_path)
		return subprocess.call([ config.VIDEO_PLAYER, video_path ]), 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

def stop_video(video_path):

	try:
		print("DEBUG: Stopping video '%s'" % video_path)
		return subprocess.call([ 'killall', config.VIDEO_PLAYER ]), 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

def open_door(pin):

	print("DEBUG: Opening door with pin %d" % pin)

	try:
		ret = 0
		if config.RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			ret = GPIO.output(pin, True)

		return ret, 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

def close_door(pin):

	print("DEBUG: Closing door with pin %d" % pin)

	try:
		ret = 0
		if config.RUNNING_ON_PI:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(pin, GPIO.OUT)
			ret = GPIO.output(pin, False)

		return ret, 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

