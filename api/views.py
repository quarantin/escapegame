# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from constance import config

from escapegame import libraspi
from escapegame.models import EscapeGameRoom, EscapeGameChallenge

from controllers.models import RaspberryPi, RemoteChallengePin, RemoteDoorPin

from multimedia.models import Video

import json
import traceback


"""
	Challenge controls, no login required for now (REST API)
"""
def set_challenge_state(request, game_slug, room_slug, challenge_slug, action):

	method = 'api.views.set_challenge_state'

	try:
		if action not in [ 'validate', 'reset' ]:
			raise Exception('Invalid action: %s' % action)

		validated = (action == 'validate')

		game = EscapeGame.objects.get(slug=game_slug)
		room = EscapeGameRoom.objects.get(slug=room_slug, escapegame=game)
		chall = EscapeGameChallenge.objects.get(slug=challenge_slug, room=room)

		status_message = chall.set_solved(validated)

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
def set_door_locked(request, game_slug, room_slug, action):

	method = 'api.views.set_door_locked'
	locked = (action == 'lock')

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s`' % action)

		game = EscapeGame.objects.get(slug=game_slug)
		room = EscapeGameRoom.objects.get(slug=room_slug, escapegame=game)

		status, message = room.set_door_locked(locked)

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
	Video controls, no login required for now (REST API)
"""

def set_video_state(request, video_slug, action):

	method = 'api.views.set_video_state'

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` for method api.views.set_video_state().' % action)

		video = Video.objects.get(slug=video_slug)

		status, message = libraspi.video_control(action, video)

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

