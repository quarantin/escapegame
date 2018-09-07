# -*- coding: utf-8 -*-

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
	('raspberry_pis', RaspberryPi),
	('escapegames', EscapeGame),
	('rooms', EscapeGameRoom),
	('challenges', EscapeGameChallenge),
]

top_fields = [
	'id',
	'slug',
	'name',
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


# JSON Import/Export models and forms

class JsonImport(models.Model):
	json_configuration = models.FileField()

	def save(self, *args, **kwargs):
		pass

	class Meta:
		verbose_name = 'JSON Import'
		verbose_name_plural = 'JSON Import'

class JsonImportForm(forms.ModelForm):

	class Meta:
		model = JsonImport
		fields = [
			'json_configuration',
		]

	def json_import (self, model, dic):

		try:
			try:
				obj = model.objects.get(id=dic['id'])
				for key, val in dic.items():
					setattr(obj, key, val)
			except:
				obj = model(**dic)

			obj.save()

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s<br>\n%s' % err

	def json_import_list(self, model, listdic):

		try:
			for dic in listdic:
				status, message = self.json_import(model, dic)
				if status != 0:
					return status, message

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % err

	def load(self, json_configuration):

		try:
			databytes = bytearray()
			for chunk in json_configuration.chunks():
				databytes += chunk

			status, message = 0, 'Success'
			config = json.loads(databytes.decode('utf-8').strip())

			for jsonkey, model in model_mapping:
				if jsonkey in config:
					status, message = self.json_import_list(model, config[jsonkey])
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
	escapegames = models.BooleanField(default=True)
	rooms = models.BooleanField(default=True)
	challenges = models.BooleanField(default=True)
	raspberry_pis = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		pass

	class Meta:
		verbose_name = 'JSON Export'
		verbose_name_plural = 'JSON Export'

class JsonExportForm(forms.ModelForm):

	class Meta:
		model = JsonExport
		fields = [
			'indent',
			'export_date',
			'software_version',
			'images',
			'videos',
			'escapegames',
			'rooms',
			'challenges',
			'raspberry_pis',
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
				config[jsonkey] = get_sorted_query_set(model.objects.all().order_by('id').values(), [ 'locked', 'solved' ])

		return config
