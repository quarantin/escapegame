# -*- coding: utf-8 -*-

from django.db.models import Q
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from controllers.models import ChallengeGPIO, DoorGPIO, LiftGPIO, RaspberryPi
from multimedia.models import Image, MultimediaFile
from .models import EscapeGame, EscapeGameCube, EscapeGameRoom, EscapeGameChallenge
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
	raspberry_pis = game.get_controllers()
	videos = game.get_multimedia_files(MultimediaFile.TYPE_VIDEO)
	audios = game.get_multimedia_files(MultimediaFile.TYPE_AUDIO)

	for room in rooms:
		room.url_callback = '/%s/api/door/%s/%s' % (lang, game.slug, room.slug)
		room.challs = EscapeGameChallenge.objects.filter(room=room)
		for chall in room.challs:
			chall.url_callback = '/%s/api/challenge/%s/%s/%s' % (lang, game.slug, room.slug, chall.slug)

	game.lifts = []
	cubes = EscapeGameCube.objects.filter(game=game)
	for cube in cubes:
		lifts = LiftGPIO.objects.filter(cube=cube)
		for lift in lifts:
			lift.url_callback = '/%s/api/lift/%s/%s' % (lang, game.slug, lift.slug)
			game.lifts.append(lift)

	for raspi in raspberry_pis:

		success = ('[ ONLINE ]', 'success', 'danger')
		failure = ('[ OFFLINE ]', 'danger', 'success')

		raspi.status, raspi.badge, raspi.not_badge = raspi.online and success or failure

	context = {
		'game': game,
		'rooms': rooms,
		'videos': videos,
		'audios': audios,
		'raspberry_pis': raspberry_pis,
	}

	template = loader.get_template('escapegame/escapegame.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame_reset(request, game_slug):

	method = 'escapegame.views.escapegame_reset'

	try:
		game = EscapeGame.objects.get(slug=game_slug)
		print('Reseting escape game %s' % game.name)

		game.reset()

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
		game = EscapeGame.objects.get(slug=game_slug)
		raspis = game.get_controllers(as_dict=True)
		cubes = EscapeGameCube.objects.filter(game=game)

		game = EscapeGame.objects.filter(slug=game_slug).values().get()
		game['videos'] = [ x for x in MultimediaFile.objects.filter(media_type='video').values() ]
		game['audios'] = [ x for x in MultimediaFile.objects.filter(media_type='audio').values() ]
		game['raspberrypis'] = raspis
		game['rooms'] = []
		game['lifts'] = []

		for raspi in game['raspberrypis']:

			success = ('[ ONLINE ]', 'success', 'danger')
			failure = ('[ OFFLINE ]', 'danger', 'success')

			raspi['status'], raspi['badge'], raspi['not_badge'] = raspi['online'] and success or failure

		for cube in cubes:
			lifts = LiftGPIO.objects.filter(cube=cube).values()
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

	try:
		if action not in [ 'validate', 'reset' ]:
			raise Exception('Invalid action: `%s` for method: `%s`' % (action, method))

		game = EscapeGame.objects.get(slug=game_slug)
		room = EscapeGameRoom.objects.get(slug=room_slug, game=game)
		chall = EscapeGameChallenge.objects.get(slug=challenge_slug, room=room)

		status, message = chall.set_solved(request, action)
		if status != 0:
			raise Exception('call to chall.set_solved() failed with error `%s`' % message)

		libraspi.notify_frontend(game)

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
		room = EscapeGameRoom.objects.get(game=game, slug=room_slug)

		status, message = room.set_locked(request, action)

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
		cubes = EscapeGameCube.objects.filter(game=game)

		for cube in cubes:
			lift = LiftGPIO.objects.get(cube=cube, slug=lift_slug)

			status, message = lift.set_raised(raised, from_gamemaster=True)
			if status != 0:
				return JsonResponse({
					'status': 1,
					'method': method,
					'message': 'Error: %s' % err,
					'traceback': traceback.format_exc(),
				})

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
	REST media controls for audio and video files, no login required for now (REST API)
"""
def rest_media_control(request, media_slug, action):

	method = 'escapegame.views.rest_media_control'

	try:
		if action not in [ 'pause', 'play', 'stop', 'rewind', 'fast-forward', 'volume-down', 'volume-up' ]:
			raise Exception('Invalid action `%s` for method: `%s`' % (action, method))

		media = MultimediaFile.objects.get(slug=media_slug)

		status, message = media.control(action)
		if status != 0:
			return JsonResponse({
				'status': status,
				'method': method,
				'message': message,
			})

		try:
			if action == 'play':
				cube = EscapeGameCube.objects.get(briefing_media=media)
				lift = LiftGPIO.objects.get(cube=cube)
				status, message = lift.raise_lift()

				libraspi.notify_frontend()

		except EscapeGameCube.DoesNotExist:
			print('Not raising lift because no cube associated to media `%s`' % media.name)
			pass
		except LiftGPIO.DoesNotExist:
			print('Not raising lift because no lift associated to cube `%s`' % cube.name)
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
