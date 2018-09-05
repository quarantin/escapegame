# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from controllers.models import Door
from multimedia.models import Image, Video

from . import libraspi
from .tasks import cube_control
from .models import EscapeGame, EscapeGameRoom, EscapeGameChallenge

import os, subprocess, traceback

"""
	Escape Game Operator Pages
"""

@login_required
def escapegame_index(request):

	context = {
		'games': EscapeGame.objects.all(),
	}

	template = loader.get_template('escapegame/index.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame_detail(request, game_slug):

	game = EscapeGame.objects.get(slug=game_slug)
	rooms = EscapeGameRoom.objects.filter(escapegame=game)

	for room in rooms:

		host, port, protocol = libraspi.get_net_info(request, room.get_controller())

		room.url_callback = '%s://%s%s/api/door/%s/%s' % (protocol, host, port, game.slug, room.slug)

	context = {
		'game': game,
		'rooms': rooms,
	}

	template = loader.get_template('escapegame/escapegame.html')

	return HttpResponse(template.render(context, request))


@login_required
def escapegame_pause(request, game_slug):

	method = 'escapegame.views.escapegame_pause'

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		status, message = game.briefing_video.control(request, 'pause')
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

@login_required
def escapegame_start(request, game_slug):

	method = 'escapegame.views.escapegame_start'

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		status, message = game.briefing_video.play(request)
		if status != 0:
			return JsonResponse({
				'status': status,
				'method': method,
				'message': message,
				'traceback': traceback.format_exc(),
			})

		# Raise the cube: Create a background task to delay call to:
		# libraspi.cube_control('raise', game.cube.pin)
		cube_control('raise', game.cube.pin, schedule=game.cube_delay)

		return JsonResponse({
			'status': 0,
			'method': method,
			'message': 'Success',
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'method': method,
			'message': 'Error: %s' % err,
			'traceback': traceback.format_exc(),
		})

@login_required
def escapegame_reset(request, game_slug):

	method = 'escapegame.views.escapegame_reset'

	try:
		game = EscapeGame.objects.get(slug=game_slug)
		rooms = EscapeGameRoom.objects.filter(escapegame=game)
		print('Reseting escape game %s' % game.escapegame_name)

		game.reset()

		print('Closing room doors')

		# For each room
		for room in rooms:

			# Close the door
			print('Closing door for room %s' % room.room_name)
			room.start_time = None
			status, message = room.door.lock()
			if status != 0:
				return JsonResponse({
					'status': status,
					'method': method,
					'message': message,
					'traceback': traceback.format_exc(),
				})

			print('Reseting challenges')

			# Reset all challenges
			challenges = EscapeGameChallenge.objects.filter(room=room)
			for chall in challenges:

				print('Reseting challenge %s' % chall.challenge_name)
				status, message = chall.set_solved(request, False)
				if status != 0:
					return JsonResponse({
						'status': status,
						'method': method,
						'message': message,
						'traceback': traceback.format_exc(),
					})

		# Stop video player
		status, message = game.briefing_video.stop(request)

		# We don't want to return an error if the stop action failed,
		# because maybe there was no video running, in which case this
		# call should fail and we still want to continue.
		#if message != 'Success':
		#	return JsonResponse({
		#		'status': status,
		#		'message': message,
		#	})

		print('Done reseting escapegame %s' % game.escapegame_name)

		return JsonResponse({
			'status': 0,
			'method': method,
			'message': 'Success',
		})

	except Exception as err:
		print('Failed reseting escapegame %s' % game.escapegame_name)
		return JsonResponse({
			'status': 1,
			'method': method,
			'message': 'Error: %s' % err,
			'traceback': traceback.format_exc(),
		})

def __populate_images(obj, key):
	pk = '%s_id' % key
	if pk in obj and obj[pk]:
		obj[key] = Image.objects.values().get(pk=obj[pk])
		del obj[key]['id']
		del obj[pk]

@login_required
def escapegame_status(request, game_slug):

	method = 'escapegame.views.escapegame_status'

	try:
		game = EscapeGame.objects.values().get(slug=game_slug)
		game['rooms'] = []

		__populate_images(game, 'map_image')

		rooms = EscapeGameRoom.objects.filter(escapegame=game['id']).values()
		for room in rooms:

			room['challenges'] = []
			room['door'] = Door.objects.filter(pk=room['door_id']).values().get()
			challs = EscapeGameChallenge.objects.filter(room=room['id']).values()
			for chall in challs:
				__populate_images(chall, 'challenge_solved_image')
				room['challenges'].append(chall)

			__populate_images(room, 'door_image')
			game['rooms'].append(room)

		game['status'] = 0
		game['method'] = method
		game['message'] = 'Success'

		return JsonResponse(game)

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'method': method,
			'message': 'Error: %s' % err,
			'traceback': traceback.format_exc(),
		});

"""
	REST challenge controls, no login required for now (REST API)
"""
def rest_challenge_control(request, game_slug, room_slug, challenge_slug, action):

	method = 'escapegame.views.rest_challenge_control'
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

	method = 'escapegame.views.rest_door_control'
	locked = (action == 'lock')

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s` for method: `%s`' % (action, method))

		game = EscapeGame.objects.get(slug=game_slug)
		room = EscapeGameRoom.objects.get(slug=room_slug, escapegame=game)

		status, message = room.door.set_locked(locked)

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

	method = 'escapegame.views.rest_video_control'

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
