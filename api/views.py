# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from constance import config

from escapegame import libraspi
from escapegame.models import RaspberryPi, RemoteChallengePin, RemoteDoorPin

from .models import RestToken

import json, socket, traceback


"""
	REST Token Authentication
"""
@csrf_exempt
def get_token(request):

	method = 'get_auth_token'

	try:
		jsondata = json.loads(request.body.decode('utf-8'))

		username = jsondata['username']
		password = jsondata['password']

		message = 'Info: Invalid username or password supplied'
		user = authenticate(request, username=username, password=password)
		if user:

			message = 'Info: Token generation failed for user `%s`' % username
			token, expire = RestToken.get_token(request.META['REMOTE_ADDR'], user)
			print("TOKEN: %s, CREATED: %s, EXPIRE: %s, HOST: %s" % (token, token.created, expire, token.host))
			if token:
				return JsonResponse({
					'status': 0,
					'message': 'Success',
					'method': method,
					'expire': expire,
					'token': token.key,
				})

		return JsonResponse({
				'status': 1,
				'message': message,
				'method': method,
			})


	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % traceback.format_exc(),
			'method': method,
		})

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
			challenges = EscapeGameChallenge.objects.filter(challenge_pin=pin)
			remote_pin = RemoteChallengePin.objects.get(raspberrypi=myself, challenge__in=challenges)
			callback_url = (validated and remote_pin.url_callback_validate or remote_pin.url_callback_reset)

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
				'pin': pin,
				'locked': locked,
			})

		if config.IS_SLAVE:
			myself = RaspberryPi.objects.get(hostname='%s.local' % socket.gethostname())
			challenges = EscapeGameChallenge.objects.filter(challenge_pin=pin)
			remote_pin = RemoteDoorPin.objects.get(raspberrypi=myself, challenge__in=challenges)
			callback_url = (locked and remote_pin.url_callback_lock or remote_pin.url_callback_unlock)

			status, message = libraspi.do_get(callback_url)
			# TODO validate status and message (the content of response)

		return JsonResponse({
			'status': status,
			'message': message,
			'method': method,
			'pin': pin,
			'locked': locked,
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

"""
	Video controls, no login required for now (REST API)
"""

def set_video_state(request, video_slug, action):

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` for method set_video_state().' % action)

		video = Video.objects.get(slug=video_slug)

		if action == 'pause':
			status, message = libraspi.video_control('pause', video)

		elif action == 'play':
			status, message = libraspi.video_control('play', video)

		elif action == 'stop':
			status, message = libraspi.video_control('stop', video)

		else:
			raise Exception('Action`%s` not implemented for method set_video_state' % action)

		return JsonResponse({
			'status': status,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

