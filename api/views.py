# -*- coding: utf-8 -*-

from constance import config
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from escapegame import libraspi

import os, subprocess

"""
	Configuration, no login required for now (REST API)
"""

@csrf_exempt
def set_config(request):

	method = 'set_config'

	try:
		if request.method != 'POST':
			raise Exception('Unsupported method: %s' % request.method)
		
		callback_url = request.POST.get('callback_url')
		if not callback_url:
			raise Exception('Missing parameter \'callback_url\'')

		config.VALIDATION_URL = callback_url

		return JsonResponse({
			'status': 0,
			'message': 'Success',
			'method': method,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
			'method': method,
		})

"""
	Door controls, no login required for now (REST API)
"""
def set_door_locked(request, action, pin):

	method = 'set_door_locked'

	try:
		if action not in [ 'lock', 'unlock' ]:
			raise Exception('Invalid action: %s' % action)

		locked = (action != 'lock')

		status, message = libraspi.set_door_locked(pin, locked)

		return JsonResponse({
			'status': status,
			'message': message,
			'method': method,
		})

	except Exception as err:
		return JsonResponse({
			'status': 1,
			'message': 'Error: %s' % err,
			'method': method,
		})
