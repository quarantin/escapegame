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
def index(request):

	context = {
		'games': EscapeGame.objects.all(),
	}

	template = loader.get_template('escapegame/index.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame(request, slug):

	game = EscapeGame.objects.get(slug=slug)

	context = {
		'game': game,
		'rooms': EscapeGameRoom.objects.filter(game=game),
	}

	template = loader.get_template('escapegame/escapegame.html')

	return HttpResponse(template.render(context, request))

def escapegame_start(request, slug):

	game = EscapeGame.objects.get(slug=slug)

	status, message = libraspi.play_video(game.video_path)
	if status != 0:
		return JsonResponse({
			'status': status,
			'message': message,
		})

	status, message = libraspi.open_door(game.door_pin)
	return JsonResponse({
		'status': status,
		'message': message,
	})

def escapegame_reset(request, slug):

	""" TODO: Reset all states (doors, challenges, etc) """

	game = EscapeGame.objects.get(slug=slug)
	rooms = EscapeGameRoom.objects.filter(game=game)

	# Stop the video player
	status, message = libraspi.stop_video(game.video_path)
	if status != 0:
		return JsonResponse({
			'status': status,
			'message': message,
		})

	# Close the SAS door
	status, message = libraspi.close_door(game.door_pin)
	if status != 0:
		return JsonResponse({
			'status': status,
			'message': message,
		})

	# For each room
	for room in rooms:

		# Close the door
		status, message = libraspi.close_door(room.door_pin)
		if status != 0:
			return JsonResponse({
				'status': status,
				'message': message,
			})

		# Reset all the challenges
		challenges = EscapeGameChallenge.objects.filter(room=room)
		for chall in challenges:
			print("DEBUG: Reseting challenge %s" % chall)
			chall.solved = False
			chall.save()

	return JsonResponse({
		'status': status,
		'message': message,
	})
	
"""
	Video Handling, no login required for now (REST)
"""

def video_play(request, slug):

	game = EscapeGame.objects.get(slug=slug)

	status, message = libraspi.play_video(game.video_path)

	return JsonResponse({
		'status': status,
		'message': message,
	})

def video_stop(request, slug):

	game = EscapeGame.objects.get(slug=slug)

	status, message = libraspi.stop_video(game.video_path)

	return JsonResponse({
		'status': status,
		'message': message,
	})

"""
	Door Handling, no login required for now (REST)
"""

def door_status(request, slug, pin=-1):

	if pin == -1:
		game = EscapeGame.objects.get(slug=slug)
		pin = game.door_pin

	return JsonResponse({
		'status': 0,
		'message': 'Success',
	})

def door_open(request, slug, pin=-1):

	if pin == -1:
		game = EscapeGame.objects.get(slug=slug)
		pin = game.door_pin

	status, message = libraspi.open_door(pin)

	return JsonResponse({
		'status': status,
		'message': message,
	})

def door_close(request, slug, pin=-1):

	if pin == -1:
		game = EscapeGame.objects.get(slug=slug)
		pin = game.door_pin

	status, message = libraspi.close_door(pin)

	return JsonResponse({
		'status': status,
		'message': message,
	})

"""
	Challenge handling, no login requried for now (REST)
"""
@login_required
def challenge_status(request, slug):

	try:
		game = EscapeGame.objects.get(slug=slug)

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
			newroom['door_pin_opened'] = room.door_pin_opened

			result['rooms'].append(newroom)

		result['status'] = 0
		result['message'] = 'Success'

		return JsonResponse(result)

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
		});

@login_required
def challenge_solve(request, slug, challenge):

	return JsonResponse({
		'status': 1,
		'message': 'Not implemented!',
	})

@login_required
def challenge_reset(request, slug, challenge):

	return JsonResponse({
		'status': 1,
		'message': 'Not implemented!',
	})
