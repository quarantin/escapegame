from django import forms
from django.db import models

from escapegame import libraspi

from datetime import datetime

from collections import OrderedDict

from escapegame.models import *

import json

model_mapping = [
	('images', Image),
	('videos', Video),
	('escapegames', EscapeGame),
	('rooms', EscapeGameRoom),
	('challenges', EscapeGameChallenge),
	('raspberry_pis', RaspberryPi),
	('remote_challenge_pins', RemoteChallengePin),
	('remote_door_pins', RemoteChallengePin),
	('remote_led_pins', RemoteChallengePin),
]

top_fields = [
	'id',
	'slug',
	'name',
	'escapegame_name',
	'room_name',
	'challenge_name',
	'escapegame_id',
	'room_id',
	'challenge_id',
	'raspberrypi_id',
]

def get_sorted_query_set(queryset, excluded_fields):

	result = []

	for obj in queryset:
		objdict = OrderedDict()

		# Add top fields first
		for top_field in top_fields:
			if top_field in obj:
				val = obj.pop(top_field)
				if val != None:
					objdict[top_field] = val

		# Then add remaining fields in alphabetical order, except the excluded ones.
		for key in sorted(obj.keys()):

			excluded = False
			for excluded_field in excluded_fields:
				if key.endswith(excluded_field):
					excluded = True
					break

			if not excluded:
				val = obj[key]
				if val != None:
					objdict[key] = obj[key]

		result.append(objdict)

	return result

class JsonImport(models.Model):
	json_configuration = models.FileField()

	def save(self, *args, **kwargs):
		pass

class JsonImportForm(forms.ModelForm):

	class Meta:
		model = JsonImport
		fields = [
			'json_configuration',
		]

	def load(self, json_configuration):

		try:
			databytes = bytearray()
			for chunk in json_configuration.chunks():
				databytes += chunk

			status, message = 0, 'Success'
			config = json.loads(databytes.decode('utf-8').strip())

			for jsonkey, model in model_mapping:
				if jsonkey in config:
					status, message = model.json_import_list(config[jsonkey])
					if status != 0:
						return status, message

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

class JsonExport(models.Model):
	indent = models.BooleanField(default=True)
	export_date = models.BooleanField(default=True)
	software_version = models.BooleanField(default=True)
	images = models.BooleanField(default=True)
	videos = models.BooleanField(default=True)
	video_players = models.BooleanField(default=True)
	escapegames = models.BooleanField(default=True)
	rooms = models.BooleanField(default=True)
	challenges = models.BooleanField(default=True)
	raspberry_pis = models.BooleanField(default=True)
	remote_challenge_pins = models.BooleanField(default=True)
	remote_door_pins = models.BooleanField(default=True)
	remote_led_pins = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		pass

class JsonExportForm(forms.ModelForm):

	class Meta:
		model = JsonExport
		fields = [
			'indent',
			'export_date',
			'software_version',
			'images',
			'videos',
			'video_players',
			'escapegames',
			'rooms',
			'challenges',
			'raspberry_pis',
			'remote_challenge_pins',
			'remote_door_pins',
			'remote_led_pins',
		]

	def dump(self, post):

		now = datetime.now()

		config = OrderedDict()

		# Check if we should beautify JSON
		config['indent'] = False
		if post.get('indent'):
			config['indent'] = True

		# Export the date of current export
		if post.get('export_date'):
			config['export_date'] = now.strftime('%Y-%m-%d %H:%M:%S')

		# Export the software version
		if post.get('software_version'):
			config['software_version'] = libraspi.git_version()[:8]

		# Export the filename
		config['filename'] = 'escapegame-config-%s.json' % now.strftime('%Y-%m-%d_%H-%M-%S')

		for jsonkey, model in model_mapping:
			if post.get(jsonkey):
				config[jsonkey] = get_sorted_query_set(model.objects.all().order_by('id').values(), [ 'door_locked', 'state' ])

		return config
