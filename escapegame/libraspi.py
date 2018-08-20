# -*- coding: utf-8 -*-

from constance import config

from siteconfig import settings

from escapegame.apps import EscapegameConfig as AppConfig
logger = AppConfig.logger

import os, sys, subprocess, time
import requests

if config.RUNNING_ON_PI:
	import RPi.GPIO as GPIO

def is_running_on_pi():
	return ' '.join(os.uname()).strip().endswith('armv7l')

def do_get(url):
	try:
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
		output = subprocess.check_output([ 'git', 'rev-parse', 'HEAD' ], cwd=settings.BASE_DIR)
		return output.decode('utf-8').strip()

	except Exception as err:
		return 1, 'Error: %s' % err

def local_video_control(action, video):

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` in method video_control()' % action)

		fifo = '/tmp/%s.fifo' % video.slug

		if action == 'pause':

			fout = open(fifo, 'w')
			if not fout:
				return 1, 'No such file or directory: %s' % fifo

			fout.write('p')
			fout.close()

			return 0, 'Success'

		elif action == 'play':

			video_path = os.path.join(config.UPLOAD_VIDEO_PATH, video.video_path.path)

			if not os.path.exists(fifo):
				os.mkfifo(fifo)

			print("Playing video '%s'" % video_path)
			if config.VIDEO_PLAYER == '/usr/bin/mpv':
				status = subprocess.call([ config.VIDEO_PLAYER, '--input-file', fifo, video_path ])
			else:
				process = subprocess.Popen([ '/bin/cat', fifo ], stdout=subprocess.PIPE)
				status = subprocess.call([ config.VIDEO_PLAYER, video_path ], stdin=process.stdout)
				process.wait()

			return status, 'Success'

		elif action == 'stop':
			print("Stopping video '%s'" % video_path)
			status = subprocess.call([ 'killall', config.VIDEO_PLAYER ])
			return status, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

def remote_video_control(action, video):

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` in method remote_video_control()' % action)

		raspi = video.raspberrypi

		host = raspi.host
		port = raspi.port != 80 and ':%d' % raspi.port or ''

		url = 'http://%s%s/video/%s/%s/' % (host, port, video.slug, action)

		return do_get(url)

	except Exception as err:
		return 1, 'Error: %s' % err

def video_control(action, video):

	method = local_video_control
	if video.raspberrypi:
		method = remote_video_control

	method(action, video)

def get_pin_state(pin):

	try:
		state = 0
		if config.RUNNING_ON_PI:
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
		if config.RUNNING_ON_PI:
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
		if config.RUNNING_ON_PI:
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
		if config.RUNNING_ON_PI:
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
