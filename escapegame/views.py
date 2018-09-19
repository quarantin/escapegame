# -*- coding: utf-8 -*-

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from controllers.models import ChallengeGPIO, DoorGPIO, LiftGPIO, RaspberryPi
from multimedia.models import Image, Video
from .models import EscapeGame, EscapeGameRoom, EscapeGameChallenge
from escapegame import libraspi

import os
import traceback
import subprocess


"""
	Escape Game Operator Pages
"""

def escapegame_ping(request):
	return HttpResponse('OK')

@login_required
def escapegame_index(request):

	context = {
		'games': EscapeGame.objects.all(),
	}

	template = loader.get_template('escapegame/index.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame_detail(request, game_slug):

	lang = request.LANGUAGE_CODE
	game = EscapeGame.objects.get(slug=game_slug)
	rooms = EscapeGameRoom.objects.filter(game=game)
	raspberry_pis = RaspberryPi.objects.all()
	videos = game.get_videos()
	#videos = Video.objects.all()

	for room in rooms:
		room.url_callback = '/%s/api/door/%s/%s' % (lang, game.slug, room.slug)
		room.challs = EscapeGameChallenge.objects.filter(room=room)
		for chall in room.challs:
			chall.url_callback = '/%s/api/challenge/%s/%s/%s' % (lang, game.slug, room.slug, chall.slug)

	game.doors = DoorGPIO.objects.filter(game=game)
	for door in game.doors:
		door.url_callback = '/%s/api/door/%s/%s' % (lang, game.slug, door.slug)

	game.lifts = LiftGPIO.objects.filter(game=game)
	for lift in game.lifts:
		lift.url_callback = '/%s/api/lift/%s/%s' % (lang, game.slug, lift.slug)

	for raspi in raspberry_pis:

		success = ('[ ONLINE ]', 'success', 'danger')
		failure = ('[ OFFLINE ]', 'danger', 'success')

		raspi.status, raspi.badge, raspi.not_badge = raspi.online and success or failure

	context = {
		'game': game,
		'rooms': rooms,
		'videos': videos,
		'raspberry_pis': raspberry_pis,
	}

	template = loader.get_template('escapegame/escapegame.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame_reset(request, game_slug):

	method = 'escapegame.views.escapegame_reset'

	try:
		game = EscapeGame.objects.get(slug=game_slug)
		rooms = EscapeGameRoom.objects.filter(game=game)
		print('Reseting escape game %s' % game.name)

		game.reset()

		# Stop video player
		status, message = game.briefing_video.stop()

		# We don't want to return an error if the stop action failed,
		# because maybe there was no video running, in which case this
		# call will fail but we're still good to go.
		#if message != 'Success':
		#	return JsonResponse({
		#		'status': status,
		#		'method': method,
		#		'message': message,
		#	})

		return JsonResponse({
			'status': 0,
			'method': method,
			'message': 'Success',
		})

	except Exception as err:
		print('Failed reseting escapegame %s' % game.name)
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
		game = EscapeGame.objects.filter(slug=game_slug).values().get()
		game['raspberrypis'] = [ x for x in RaspberryPi.objects.values() ]
		game['rooms'] = []
		game['doors'] = []
		game['lifts'] = []

		for raspi in game['raspberrypis']:

			success = ('[ ONLINE ]', 'success', 'danger')
			failure = ('[ OFFLINE ]', 'danger', 'success')

			raspi['status'], raspi['badge'], raspi['not_badge'] = raspi['online'] and success or failure

		doors = DoorGPIO.objects.filter(game=game['id']).values()
		for door in doors:
			__populate_images(door, 'image')
			game['doors'].append(door)

		lifts = LiftGPIO.objects.filter(game=game['id']).values()
		for lift in lifts:
			game['lifts'].append(lift)

		__populate_images(game, 'map_image')

		rooms = EscapeGameRoom.objects.filter(game=game['id']).values()
		for room in rooms:

			room['challenges'] = []
			room['door'] = DoorGPIO.objects.filter(pk=room['door_id']).values().get()

			challs = EscapeGameChallenge.objects.filter(room=room['id']).values()
			for chall in challs:

				gpio = ChallengeGPIO.objects.filter(pk=chall['gpio_id']).values().get()
				chall['solved'] = gpio['solved']

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
		room = EscapeGameRoom.objects.get(slug=room_slug, game=game)
		chall = EscapeGameChallenge.objects.get(slug=challenge_slug, room=room)

		status, message = chall.set_solved(request, game_slug, room_slug, action)
		if status != 0:
			raise Exception('call to chall.set_solved() failed with error `%s`' % message)

		status, message = libraspi.notify_frontend(game)

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

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action `%s` for method: `%s`' % (action, method))

		game = EscapeGame.objects.get(slug=game_slug)

		try:
			room = EscapeGameRoom.objects.get(slug=room_slug, game=game)
			door = room.door
		except EscapeGameRoom.DoesNotExist:
			door = DoorGPIO.objects.get(slug=room_slug, game=game)

		status, message = door.forward_lock_request(request, game_slug, room_slug, action)

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

def rest_lift_control(request, game_slug, lift_slug, action):

	method = 'escapegame.views.rest_lift_control'

	try:
		if action not in [ 'lower', 'raise' ]:
			raise Exception('Invalid action `%s` for method: `%s`' % (action, method))

		raised = (action == 'raise')

		game = EscapeGame.objects.get(slug=game_slug)
		lift = LiftGPIO.objects.get(game=game, slug=lift_slug)

		status, message = lift.set_raised(raised, from_gamemaster=True)

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

		status, message = video.control(action)
		if status != 0:
			return JsonResponse({
				'status': status,
				'method': method,
				'message': message,
			})

		try:
			lift = LiftGPIO.objects.get(video=video)
			status, message = lift.raise_lift()

		except LiftGPIO.DoesNotExist:
			pass

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
