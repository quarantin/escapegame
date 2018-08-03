# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

import os, subprocess

from .models import EscapeGame, EscapeGameRoom, EscapeGameChallenge

from escapegame import libraspi

"""
	Escape Game Operator Pages
"""

@login_required
def selector_index(request):

	context = {
		'games': EscapeGame.objects.all(),
	}

	template = loader.get_template('escapegame/index.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame_index(request, game_slug):

	game = EscapeGame.objects.get(slug=game_slug)

	context = {
		'game': game,
		'rooms': EscapeGameRoom.objects.filter(game=game),
	}

	template = loader.get_template('escapegame/escapegame.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame_start(request, game_slug):

	game = EscapeGame.objects.get(slug=game_slug)

	status, message = libraspi.play_video(game.video_path)
	if status != 0:
		return JsonResponse({
			'status': status,
			'message': message,
		})

	status, message = game.set_sas_door_locked(False)
	if status != 0:
		return JsonResponse({
			'status': status,
			'message': message,
		})

	status, message = game.set_corridor_door_locked(False)
	return JsonResponse({
		'status': status,
		'message': message,
	})

@login_required
def escapegame_reset(request, game_slug):

	game = EscapeGame.objects.get(slug=game_slug)
	rooms = EscapeGameRoom.objects.filter(game=game)

	# Stop video player
	status, message = libraspi.stop_video(game.video_path)
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
		'status': status,
		'message': message,
	})

@login_required
def escapegame_status(request, game_slug):

	try:
		game = EscapeGame.objects.get(slug=game_slug)

		result = {}
		result['name'] = game.name
		result['slug'] = game.slug
		result['rooms'] = []

		rooms = EscapeGameRoom.objects.filter(game=game)
		for room in rooms:

			newroom = {}
			newroom['challenges'] = []

			challs = EscapeGameChallenge.objects.filter(room=room)
			for chall in challs:

				newchall = {}
				newchall['name'] = chall.name
				newchall['slug'] = chall.slug
				newchall['solved'] = chall.solved

				newroom['challenges'].append(newchall)

			newroom['name'] = room.name
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

	play = (action == 'play')
	game = EscapeGame.objects.get(slug=game_slug)

	if play:
		status, message = libraspi.play_video(game.video_path)
	else:
		status, message = libraspi.stop_video(game.video_path)

	return JsonResponse({
		'status': status,
		'message': message,
	})

"""
	Door controls, no login required for now (REST API)
"""

def set_door_locked(request, game_slug, room_slug, action):

	try:
		locked = (action == 'lock')
		game = EscapeGame.objects.get(slug=game_slug)

		if room_slug == 'sas':
			status, message = game.set_sas_door_locked(locked)

		elif room_slug == 'corridor':
			status, message = game.set_corridor_door_locked(locked)

		else:
			room = EscapeGameRoom.objects.get(slug=room_slug, game=game)
			status, message = room.set_door_locked(locked)

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
	Challenge controls, no login requried for now (REST API)
"""

@login_required
def set_challenge_status(request, game_slug, challenge_slug, action):

	try:
		solved = (action == 'solve')
		game = EscapeGame.objects.get(slug=game_slug)
		chall = EscapeGameChallenge.objects.get(slug=challenge_slug, game=game)

		status, message = chall.set_solved(solved)

		return JsonResponse({
			'status': status,
			'message': message,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		})
