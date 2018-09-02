# -*- coding: utf-8 -*-

from django.http import JsonResponse

from escapegame.models import EscapeGame, EscapeGameRoom, EscapeGameChallenge

from multimedia.models import Video

import traceback


"""
	REST challenge controls, no login required for now (REST API)
"""
def rest_challenge_control(request, game_slug, room_slug, challenge_slug, action):

	method = 'api.views.rest_challenge_control'
	validated = (action == 'validate')

	try:
		if action not in [ 'validate', 'reset' ]:
			raise Exception('Invalid action: `%s` for method: `%s`' % (action, method))

		game = EscapeGame.objects.get(slug=game_slug)
		room = EscapeGameRoom.objects.get(slug=room_slug, escapegame=game)
		chall = EscapeGameChallenge.objects.get(slug=challenge_slug, room=room)

		status, message = chall.set_solved(request, validated)

		return JsonResponse({
			'status': status,
			'method': method,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'method': method,
			'message': 'Error: %s' % err,
			'traceback': traceback.format_exc(),
		})

"""
	REST door controls, no login required for now (REST API)
"""
def rest_door_control(request, game_slug, room_slug, action):

	method = 'api.views.rest_door_control'
	locked = (action == 'lock')

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s` for method: `%s`' % (action, method))

		game = EscapeGame.objects.get(slug=game_slug)
		room = EscapeGameRoom.objects.get(slug=room_slug, escapegame=game)

		status, message = room.set_door_locked(locked)

		return JsonResponse({
			'status': status,
			'method': method,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'method': method,
			'message': 'Error: %s' % err,
			'traceback': traceback.format_exc(),
		})

"""
	REST video controls, no login required for now (REST API)
"""
def rest_video_control(request, video_slug, action):

	method = 'api.views.rest_video_control'

	try:
		if action not in [ 'pause', 'play', 'stop' ]:
			raise Exception('Invalid action `%s` for method: `%s`' % (action, method))

		video = Video.objects.get(slug=video_slug)

		status, message = video.control(request, action)

		return JsonResponse({
			'status': status,
			'method': method,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'method': method,
			'message': 'Error: %s' % err,
			'traceback': traceback.format_exc(),
		})

