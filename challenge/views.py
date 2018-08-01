# -*- coding: utf-8 -*-

from django.http import JsonResponse

from escapegame.models import EscapeGame, EscapeGameRoom, EscapeGameChallenge

def reset_challenge(request, challenge):
	return JsonResponse({ 'status': 'OK' })

def solve_challenge(request, challenge):
	return JsonResponse({ 'status': 'OK' })

def status_challenge(request, gameid):

	game = EscapeGame.objects.get(id=gameid)

	result = {}
	result['name'] = game.name
	result['rooms'] = []

	rooms = EscapeGameRoom.objects.filter(game=game)
	for room in rooms:

		newroom = {}
		newroom['name'] = room.name
		newroom['challenges'] = []

		challs = EscapeGameChallenge.objects.filter(room=room)
		for chall in challs:

			newchall = {}
			newchall['name'] = chall.name
			newchall['solved'] = chall.solved

			newroom['challenges'].append(newchall)

		result['rooms'].append(newroom)

	return JsonResponse(result)
