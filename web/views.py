# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from constance import config

from multimedia.models import Image
from escapegame.models import EscapeGame, EscapeGameRoom, EscapeGameChallenge, RemoteDoorPin

from escapegame.models import notify_frontend

from escapegame import libraspi

from .tasks import cube_control

import os, subprocess, traceback


"""
	Escape Game Operator Pages
"""

@login_required
def selector_index(request):

	context = {
		'games': EscapeGame.objects.all(),
	}

	template = loader.get_template('web/index.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame_index(request, game_slug):

	game = EscapeGame.objects.get(slug=game_slug)
	rooms = EscapeGameRoom.objects.filter(escapegame=game)

	host = config.MASTER_HOSTNAME
	port = config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or ''

	#game.url_callback_lock_sas = 'http://%s%s/web/%s/sas/lock/' % (host, port, game_slug)
	#game.url_callback_unlock_sas = 'http://%s%s/web/%s/sas/unlock/' % (host, port, game_slug)
	game.url_callback_lock_sas = '/web/%s/sas/lock/' % (game_slug)
	game.url_callback_unlock_sas = '/web/%s/sas/unlock/' % (game_slug)

	#game.url_callback_lock_corridor = 'http://%s%s/web/%s/corridor/lock/' % (host, port, game_slug)
	#game.url_callback_unlock_corridor = 'http://%s%s/web/%s/corridor/unlock/' % (host, port, game_slug)
	game.url_callback_lock_corridor = '/web/%s/corridor/lock/' % (game_slug)
	game.url_callback_unlock_corridor = '/web/%s/corridor/unlock/' % (game_slug)

	for room in rooms:

		raspberrypi = game.raspberrypi
		if room.raspberrypi:
			raspberrypi = room.raspberrypi

		"""
		if raspberrypi:
			remote_pins = RemoteDoorPin.objects.filter(room=room)
			for remote_pin in remote_pins:
				host = raspberrypi.hostname
				port = raspberrypi.port != 80 and ':%d' % raspberrypi.port or ''

				#room.url_callback_lock = 'http://%s%s/api/door/lock/%d/' % (host, port, room.door_pin)
				#room.url_callback_unlock = 'http://%s%s/api/door/unlock/%d/' % (host, port, room.door_pin)
				room.url_callback_lock = 'http://%s%s/web/%s/%s/lock/' % (host, port, room.escapegame.slug, room.slug)
				room.url_callback_unlock = 'http://%s%s/web/%s/%s/unlock/' % (host, port, room.escapegame.slug, room.slug)
		else:
		"""
		host = config.MASTER_HOSTNAME
		port = config.MASTER_PORT != 80 and ':%d' % config.MASTER_PORT or ''

		#room.url_callback_lock = 'http://%s%s/api/door/lock/%d/' % (host, port, room.door_pin)
		#room.url_callback_unlock = 'http://%s%s/api/door/unlock/%d/' % (host, port, room.door_pin)
		#room.url_callback_lock = 'http://%s%s/web/%s/%s/lock/' % (host, port, room.escapegame.slug, room.slug)
		#room.url_callback_unlock = 'http://%s%s/web/%s/%s/unlock/' % (host, port, room.escapegame.slug, room.slug)
		room.url_callback_lock = '/web/%s/%s/lock/' % (room.escapegame.slug, room.slug)
		room.url_callback_unlock = '/web/%s/%s/unlock/' % (room.escapegame.slug, room.slug)

	context = {
		'game': game,
		'rooms': rooms,
	}

	template = loader.get_template('web/escapegame.html')

	return HttpResponse(template.render(context, request))


"""
	REST API (no authentication required for now)
"""
@login_required
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

@login_required
def escapegame_start(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		status, message = libraspi.video_control('play', game.video)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# CHANGE REQUEST:
		# Don't open SAS and corridor doors automatically at the end of
		# the video, they will be opened manually by the game master.
		"""
		status, message = game.set_door_locked(game.sas_door_pin, False)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		status, message = game.set_door_locked(game.corridor_door_pin, False)
		"""

		# Raise the cube: Create a background task to delay call to:
		# libraspi.cube_control('raise', game.cube.pin)
		cube_control('raise', game.cube_pin, schedule=game.cube_delay)

		return JsonResponse({
			'status': 0,
			'message': 'Success',
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

@login_required
def escapegame_reset(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)
		rooms = EscapeGameRoom.objects.filter(escapegame=game)
		print('Reseting escape game %s' % game.escapegame_name)

		# Reset start time of game
		game.start_time = None
		game.finish_time = None
		game.save()
		notify_frontend(game)
		notify_frontend(game, '0:00:00')

		# Lower the cube (no need for delay)
		cube_control('lower', game.cube_pin, schedule=0)

		# Close SAS door
		print('Closing SAS door')
		status, message = game.set_door_locked(game.sas_door_pin, True)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# Close corridor door
		print('Closing corridor door')
		status, message = game.set_door_locked(game.corridor_door_pin, True)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		print('Closing room doors')

		# For each room
		for room in rooms:

			# Close the door
			print('Closing door for room %s' % room.room_name)
			room.start_time = None
			status, message = room.set_door_locked(True)
			if status != 0:
				return JsonResponse({
					'status': status,
					'message': message,
				})

			print('Reseting challenges')

			# Reset all challenges
			challenges = EscapeGameChallenge.objects.filter(room=room)
			for chall in challenges:

				print('Reseting challenge %s' % chall.challenge_name)
				status, message = chall.set_solved(False)
				if status != 0:
					return JsonResponse({
						'status': status,
						'message': message,
					})

		# Stop video player
		status, message = libraspi.video_control('stop', game.video)
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
			'message': 'Success',
		})

	except Exception as err:
		print('Failed reseting escapegame %s' % game.escapegame_name)
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})

def __populate_images(obj, key):
	pk = '%s_id' % key
	if pk in obj and obj[pk]:
		obj[key] = Image.objects.values().get(pk=obj[pk])
		del obj[key]['id']
		del obj[pk]

@login_required
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
			__populate_images(game, key)

		rooms = EscapeGameRoom.objects.filter(escapegame=game['id']).values()
		for room in rooms:

			room['challenges'] = []
			challs = EscapeGameChallenge.objects.filter(room=room['id']).values()
			for chall in challs:
				__populate_images(chall, 'challenge_solved_image')
				room['challenges'].append(chall)

			__populate_images(room, 'door_image')
			game['rooms'].append(room)

		return JsonResponse(game)

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % traceback.format_exc(),
		});

"""
	Door callback, no login required for now (REST API)
"""
def door_callback(request, game_slug, room_slug, action):

	method = 'web.views.door_callback'
	locked = (action == 'lock')

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s`' % action)

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
	Challenge callback, no login requried for now (REST API)
"""
def challenge_callback(request, game_slug, room_slug, challenge_slug, action):

	method = 'web.views.challenge_callback'
	solved = (action == 'validate')

	try:
		if action not in [ 'validate', 'reset' ]:
			raise Exception('Invalid action \'%s\'' % action)

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
