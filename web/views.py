# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from escapegame.models import EscapeGame, EscapeGameRoom, EscapeGameChallenge, RemoteDoorPin

from escapegame import libraspi

from constance import config

import os, subprocess

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

def escapegame_start(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		status, message = libraspi.play_video(game.video_brief.video_path)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		status, message = game.set_door_locked('sas', False)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		status, message = game.set_door_locked('corridor', False)
		return JsonResponse({
			'status': status,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

def escapegame_reset(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)
		rooms = EscapeGameRoom.objects.filter(escapegame=game)

		# Stop video player
		status, message = libraspi.stop_video(game.video_brief.video_path)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# Close SAS door
		status, message = game.set_sas_door_locked(True)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# Close corridor door
		status, message = game.set_corridor_door_locked(True)
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

def escapegame_status(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		result = {}
		result['name'] = game.escapegame_name
		result['slug'] = game.slug
		result['sas_door_locked'] = game.sas_door_locked
		result['corridor_door_locked'] = game.corridor_door_locked
		result['rooms'] = []

		rooms = EscapeGameRoom.objects.filter(escapegame=game)
		for room in rooms:

			newroom = {}
			newroom['challenges'] = []

			challs = EscapeGameChallenge.objects.filter(room=room)
			for chall in challs:

				newchall = {}
				newchall['name'] = chall.challenge_name
				newchall['slug'] = chall.slug
				newchall['solved'] = chall.solved

				newroom['challenges'].append(newchall)

			newroom['name'] = room.room_name
			newroom['slug'] = room.slug
			newroom['door_pin'] = room.door_pin
			newroom['door_locked'] = room.door_locked

			result['rooms'].append(newroom)

		result['status'] = 0
		result['message'] = 'Success'

		return JsonResponse(result)

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		});

"""
	Video controls, no login required for now (REST API)
"""

def set_video_state(request, game_slug, action):

	try:
		play = (action == 'play')

		game = EscapeGame.objects.get(slug=game_slug)

		if play:
			status, message = libraspi.play_video(game.video_brief.video_path)
		else:
			status, message = libraspi.stop_video(game.video_brief.video_path)

		return JsonResponse({
			'status': status,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

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
