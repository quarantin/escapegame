from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from escapegame.models import *

import json

from datetime import datetime

from collections import OrderedDict

def get_sorted_query_set(queryset):

	result = []

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

	for obj in queryset:
		objdict = OrderedDict()

		# Add top fields first
		for top_field in top_fields:
			if top_field in obj:
				val = obj.pop(top_field)
				#if top_field in [ 'room_id' ]:
				#	top_field = top_field.replace('_id', '')
				if val != None:
					objdict[top_field] = val

		# Then add remaining fields in alphabetical order...
		for key in sorted(obj.keys()):
			# But we don't want to export the state of challenges and door locks.
			if not key.endswith('door_locked') and not key.endswith('solved'):
				val = obj[key]
				if val != None:
					objdict[key] = obj[key]

		result.append(objdict)

	return result
	
class JsonImportForm(forms.Form):
	json_configuration = forms.FileField(label='Upload JSON')

	def json_import(self, json_configuration):

		model_mapping = [
			('images', Image),
			('videos', Video),
			('video_players', VideoPlayer),
			('escapegames', EscapeGame),
			('rooms', EscapeGameRoom),
			('challenges', EscapeGameChallenge),
			('raspberry_pis', RaspberryPi),
			('remote_challenge_pins', RemoteChallengePin),
			('remote_door_pins', RemoteChallengePin),
			('remote_led_pins', RemoteChallengePin),
		]

		try:
			databytes = bytearray()
			for chunk in json_configuration.chunks():
				databytes += chunk

			status, message = 0, 'Success'
			config = json.loads(databytes.decode('utf-8').strip())

			for mapping in model_mapping:
				jsonkey, model = mapping
				if jsonkey in config:
					status, message = model.json_import_list(config[jsonkey])
					if status != 0:
						return status, message

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % err

class JsonExportForm(forms.Form):
	indent = forms.BooleanField(label='Indent JSON', required=False)
	export_date = forms.BooleanField(label='Export date', required=False)
	software_version = forms.BooleanField(label='Software version', required=False)
	images = forms.BooleanField(label='Images', required=False)
	videos = forms.BooleanField(label='Videos', required=False)
	video_players = forms.BooleanField(label='Video players', required=False)
	escapegames = forms.BooleanField(label='Escape games', required=False)
	rooms = forms.BooleanField(label='Rooms', required=False)
	challenges = forms.BooleanField(label='Challenges', required=False)
	raspberry_pis = forms.BooleanField(label='Raspberry Pis', required=False)
	remote_challenge_pins = forms.BooleanField(label='Remote challenge pins', required=False)
	remote_door_pins = forms.BooleanField(label='Remote door pins', required=False)
	remote_led_pins = forms.BooleanField(label='Remote LED pins', required=False)

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

		# Export the filename
		config['filename'] = 'escapegame-config-%s.json' % now.strftime('%Y-%m-%d_%H-%M-%S')

		# Export images
		if post.get('images'):
			config['images'] = get_sorted_query_set(Image.objects.all().order_by('id').values())

		# Export videos
		if post.get('videos'):
			config['videos'] = get_sorted_query_set(Video.objects.all().order_by('id').values())

		# Export video players
		if post.get('video_players'):
			config['video_players'] = get_sorted_query_set(VideoPlayer.objects.all().order_by('id').values())

		# Export escape games
		if post.get('escapegames'):
			config['escapegames'] = get_sorted_query_set(EscapeGame.objects.all().order_by('id').values())

		# Export rooms
		if post.get('rooms'):
			config['rooms'] = get_sorted_query_set(EscapeGameRoom.objects.all().order_by('id').values())

		# Export challenges
		if post.get('challenges'):
			config['challenges'] = get_sorted_query_set(EscapeGameChallenge.objects.all().order_by('id').values())

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

		return config


# TODO?

"""
class JsonImportExportAdmin(admin.ModelAdmin):
	change_list_form = JsonExportForm

class Config(object):
	class Meta(object):
		app_label = 'siteconfig'
		object_name = 'Config'
		model_name = module_name = 'config'
		verbose_name_plural = _('config')
		abstract = False
		swapped = False

		def get_ordered_objects(self):
			return False

		def get_change_permission(self):
			return 'change_%s' % self.model_name

		@property
		def app_config(self):
			return apps.get_app_config(self.app_label)

		@property
		def label(self):
			return '%s.%s' % (self.app_label, self.object_name)

		@property
		def label_lower(self):
			return '%s.%s' % (self.app_label, self.model_name)

	_meta = Meta()

admin.site.register([Config], JsonImportExportAdmin)
"""
