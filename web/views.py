# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from multimedia.models import Image
from escapegame.models import EscapeGame, EscapeGameRoom, EscapeGameChallenge, RemoteDoorPin

from escapegame import libraspi

from constance import config

import os, subprocess, traceback


"""
	Escape Game Operator Pages
"""

#@login_required
def selector_index(request):

	context = {
		'games': EscapeGame.objects.all(),
	}

	template = loader.get_template('web/index.html')

	return HttpResponse(template.render(context, request))

#@login_required
def escapegame_index(request, game_slug):

	game = EscapeGame.objects.get(slug=game_slug)
	rooms = EscapeGameRoom.objects.filter(escapegame=game)

	host = config.MASTER_HOSTNAME
	port = config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or ''

	game.url_callback_lock_sas = 'http://%s%s/web/%s/sas/lock/' % (host, port, game_slug)
	game.url_callback_unlock_sas = 'http://%s%s/web/%s/sas/unlock/' % (host, port, game_slug)

	game.url_callback_lock_corridor = 'http://%s%s/web/%s/corridor/lock/' % (host, port, game_slug)
	game.url_callback_unlock_corridor = 'http://%s%s/web/%s/corridor/unlock/' % (host, port, game_slug)

	for room in rooms:

		raspberrypi = game.raspberrypi
		if room.raspberrypi:
			raspberrypi = room.raspberrypi

		if raspberrypi:
			remote_pins = RemoteDoorPin.objects.filter(room=room)
			for remote_pin in remote_pins:
				host = raspberrypi.hostname
				port = raspberrypi.port != 80 and ':%d' % raspberrypi.port or ''

				room.url_callback_lock = 'http://%s%s/api/door/lock/%d/' % (host, port, room.door_pin)
				room.url_callback_unlock = 'http://%s%s/api/door/unlock/%d/' % (host, port, room.door_pin)
		else:
			host = config.MASTER_HOSTNAME
			port = config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or ''

			room.url_callback_lock = 'http://%s%s/api/door/lock/%d/' % (host, port, room.door_pin)
			room.url_callback_unlock = 'http://%s%s/api/door/unlock/%d/' % (host, port, room.door_pin)

	context = {
		'game': game,
		'rooms': rooms,
	}

	template = loader.get_template('web/escapegame.html')

	return HttpResponse(template.render(context, request))


"""
	REST API (no authentication required for now)
"""

def escapegame_pause(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		status, message = libraspi.video_control('pause', game.video)
		return JsonResponse({
			'status': status,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

def escapegame_start(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		status, message = libraspi.video_control('play', game.video)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		status, message = game.set_door_locked(game.sas_door_pin, False)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		status, message = game.set_door_locked(game.corridor_door_pin, False)
		return JsonResponse({
			'status': status,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

def escapegame_stop(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)
		rooms = EscapeGameRoom.objects.filter(escapegame=game)

		# Stop video player
		status, message = libraspi.video_control('stop', game.video)
		if message != 'Success':
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# Close SAS door
		status, message = game.set_door_locked(game.sas_door_pin, True)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# Close corridor door
		status, message = game.set_door_locked(game.corridor_door_pin, True)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# For each room
		for room in rooms:

			# Close the door
			status, message = room.set_door_locked(True)
			if status != 0:
				return JsonResponse({
					'status': status,
					'message': message,
				})

			# Reset all challenges
			challenges = EscapeGameChallenge.objects.filter(room=room)
			for chall in challenges:

				status, message = chall.set_solved(False)
				if status != 0:
					return JsonResponse({
						'status': status,
						'message': message,
					})

		return JsonResponse({
			'status': 0,
			'message': 'Success',
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

def populate_images(obj, key):
	pk = '%s_id' % key
	if pk in obj and obj[pk]:
		obj[key] = Image.objects.values().get(pk=obj[pk])
		del obj[key]['id']
		del obj[pk]

def escapegame_status(request, game_slug):

	try:
		game = EscapeGame.objects.values().get(slug=game_slug)
		game['rooms'] = []

		image_keys = [
			'map_image',
			'sas_door_image',
			'corridor_door_image',
		]

		for key in image_keys:
			populate_images(game, key)

		rooms = EscapeGameRoom.objects.filter(escapegame=game['id']).values()
		for room in rooms:

			room['challenges'] = []
			challs = EscapeGameChallenge.objects.filter(room=room['id']).values()
			for chall in challs:
				populate_images(chall, 'challenge_solved_image')
				room['challenges'].append(chall)

			populate_images(room, 'door_unlocked_image')
			game['rooms'].append(room)

		return JsonResponse(game)

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % traceback.format_exc(),
		});

"""
	Door controls (SAS, Corridor), no login required for now (REST API)
"""

def set_door_locked(request, game_slug, room_slug, action):

	method = 'set_door_locked'

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action \'%s\'' % action)

		locked = (action == 'lock')

		game = EscapeGame.objects.get(slug=game_slug)

		if room_slug in [ 'sas', 'corridor' ]:
			status, message = game.set_door_locked(room_slug, locked)

		else:
			room = EscapeGameRoom.objects.get(slug=room_slug, escapegame=game)
			status, message = room.set_door_locked(locked)

		return JsonResponse({
			'status': status,
			'message': message,
			'method': method,
			'locked': locked,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
			'method': method,
		})

"""
	Challenge controls, no login requried for now (REST API)
"""

#@login_required
def set_challenge_status(request, game_slug, room_slug, challenge_slug, action):

	method = 'set_challenge_status'

	try:
		if action not in [ 'validate', 'reset' ]:
			raise Exception('Invalid action \'%s\'' % action)

		solved = (action == 'validate')

		game = EscapeGame.objects.get(slug=game_slug)
		room = EscapeGameRoom.objects.get(slug=room_slug, escapegame=game)
		chall = EscapeGameChallenge.objects.get(slug=challenge_slug, room=room)

		status, message = chall.set_solved(solved)

		return JsonResponse({
			'status': status,
			'message': message,
			'method': method,
			'solved': solved,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
			'method': method,
		})
