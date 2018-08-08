from django import forms

from escapegame.models import *

import json

from datetime import datetime

from collections import OrderedDict

def get_sorted_query_set(queryset):

	result = []

	top_fields = [ 'id', 'slug', 'name', 'escapegame_name', 'room_name', 'challenge_name', 'escapegame_id', 'room_id', 'challenge_id', 'raspberrypi_id' ]

	for obj in queryset:
		objdict = OrderedDict()

		for top_field in top_fields:
			if top_field in obj:
				objdict[top_field] = obj.pop(top_field)

		for key in sorted(obj.keys()):
			if not key.endswith('door_locked') and not key.endswith('solved'):
				val = obj[key]
				if val != None:
					objdict[key] = obj[key]

		result.append(objdict)

	return result
	
class JsonImportForm(forms.Form):
	json_configuration = forms.FileField(label='Upload JSON')

	def json_import(self, json_configuration):

		databytes = bytearray()
		for chunk in json_configuration.chunks():
			databytes += chunk

		config = json.loads(databytes.decode('utf-8').strip())
		# TODO write config to database

class JsonExportForm(forms.Form):
	indent = forms.BooleanField(label='Indent JSON', required=False)
	export_date = forms.BooleanField(label='Export date', required=False)
	software_version = forms.BooleanField(label='Software version', required=False)
	escapegames = forms.BooleanField(label='Escape games', required=False)
	raspberry_pis = forms.BooleanField(label='Raspberry Pis', required=False)
	remote_challenge_pins = forms.BooleanField(label='Remote challenge pins', required=False)
	remote_door_pins = forms.BooleanField(label='Remote door pins', required=False)
	remote_led_pins = forms.BooleanField(label='Remote LED pins', required=False)
	images = forms.BooleanField(label='Images', required=False)
	videos = forms.BooleanField(label='Videos', required=False)

	def json_export(self, post):

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

		# Setting the filename
		config['filename'] = 'escapegame-config-%s.json' % now.strftime('%Y-%m-%d_%H-%M-%S')

		# Export escape games, rooms, and challenges,
		if post.get('escapegames'):
			config['escapegames'] = get_sorted_query_set(EscapeGame.objects.all().order_by('id').values())
			for escapegame in config['escapegames']:
				escapegame['rooms'] = get_sorted_query_set(EscapeGameRoom.objects.filter(escapegame=escapegame['id']).order_by('id').values())
				for room in escapegame['rooms']:
					room['challenges'] = get_sorted_query_set(EscapeGameChallenge.objects.filter(room=room['id']).order_by('id').values())

		# Export Raspberry Pis
		if post.get('raspberry_pis'):
			config['raspberry_pis'] = get_sorted_query_set(RaspberryPi.objects.all().order_by('id').values())

		# Export remote challenge pins
		if post.get('remote_challenge_pins'):
			config['remote_challenge_pins'] = get_sorted_query_set(RemoteChallengePin.objects.all().order_by('id').values())

		# Export the remote door pins
		if post.get('remote_door_pins'):
			config['remote_door_pins'] = get_sorted_query_set(RemoteDoorPin.objects.all().order_by('id').values())

		# Export the remote LED pins
		if post.get('remote_led_pins'):
			config['remote_led_pins'] = get_sorted_query_set(RemoteLedPin.objects.all().order_by('id').values())

		# Export images
		if post.get('images'):
			config['images'] = get_sorted_query_set(Image.objects.all().order_by('id').values())

		# Export videos
		if post.get('videos'):
			config['videos'] = get_sorted_query_set(Video.objects.all().order_by('id').values())

		return config
