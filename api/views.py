# -*- coding: utf-8 -*-

from constance import config
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from escapegame import libraspi
from escapegame.models import RaspberryPi, RemoteChallengePin, RemoteDoorPin

import os, socket, subprocess

"""
	Challenge controls, no login required for now (REST API)
"""
def set_challenge_state(request, action, pin):

	method = 'set_challenge_state'

	try:
		if action not in [ 'validate', 'reset' ]:
			raise Exception('Invalid action: %s' % action)

		validated = (action == 'validate')

		#status, message = libraspi.set_challenge_state(pin, validated)
		#if status != 0:
		#	return JsonResponse({
		#		'status': status,
		#		'message': message,
		#		'method': method,
		#	})

		if config.IS_SLAVE:
			myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
			remote_pin = RemoteChallengePin.objects.get(raspberrypi=myself, pin_number=pin)
			callback_url = (validated and remote_pin.callback_url_validate or remote_pin.callback_url_reset)

			status, message = libraspi.do_get(callback_url)
			# TODO validate status and message (the content of response)

		return JsonResponse({
			'status': status,
			'message': message,
			'method': method,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
			'method': method,
		})

"""
	Door controls, no login required for now (REST API)
"""
def set_door_locked(request, action, pin):

	method = 'set_door_locked'

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action: %s' % action)

		locked = (action == 'lock')

		status, message = libraspi.set_door_locked(pin, locked)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
				'method': method,
			})

		if config.IS_SLAVE:
			myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
			remote_pin = RemoteDoorPin.objects.get(raspberrypi=myself, pin_number=pin)
			callback_url = (locked and remote_pin.callback_url_lock or remote_pin.callback_url_unlock)

			status, message = libraspi.do_get(callback_url)
			# TODO validate status and message (the content of response)

		return JsonResponse({
			'status': status,
			'message': message,
			'method': method,
		})


	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
			'method': method,
		})

"""
	Led controls, no login required for now (REST API)
"""
def set_led_state(request, action, pin):

	method = 'set_led_state'

	try:
		if action not in [ 'on', 'off' ]:
			raise Exception('Invalid action: %s' % action)

		onoff = (action == 'on')

		status, message = libraspi.set_led_state(pin, onff)

		return JsonResponse({
			'status': status,
			'message': message,
			'method': method,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
			'method': method,
		})

