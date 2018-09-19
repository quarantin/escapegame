# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.core import serializers

from escapegame import libraspi
from escapegame.models import *
from controllers.models import *
from multimedia.models import *

from collections import OrderedDict
from datetime import datetime
import traceback
import json


model_mapping = [
	('images', Image),
	('videos', Video),
	('controllers', Controller),
	('raspberry_pis', RaspberryPi),
	('GPIOs', GPIO),
	('cubeGPIOs', CubeGPIO),
	('liftGPIOs', LiftGPIO),
	('escapegames', EscapeGame),
	('doorGPIOs', DoorGPIO),
	('rooms', EscapeGameRoom),
	('challengeGPIOs', ChallengeGPIO),
	('challenges', EscapeGameChallenge),
]

#
# Models
#

class JsonImport(models.Model):

	class Meta:
		verbose_name = 'JSON Import'
		verbose_name_plural = 'JSON Import'

	json_configuration = models.FileField()

	def save(self, *args, **kwargs):
		pass

	@staticmethod
	def load_list(model, listdic):

		try:
			dics = json.dumps(listdic)
			objects = serializers.deserialize('json', dics)
			for obj in objects:
				obj.save()

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % traceback.format_exc()

	@staticmethod
	def load(json_configuration):

		try:
			databytes = bytearray()
			for chunk in json_configuration.chunks():
				databytes += chunk

			status, message = 0, 'Success'
			config = json.loads(databytes.decode('utf-8').strip())

			for jsonkey, model in model_mapping:
				if jsonkey in config:
					status, message = JsonImport.load_list(model, config[jsonkey])
					if status != 0:
						return status, message

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % traceback.format_exc()

class JsonExport(models.Model):

	class Meta:
		verbose_name = 'JSON Export'
		verbose_name_plural = 'JSON Export'

	indent = models.BooleanField(default=True)
	export_date = models.BooleanField(default=True)
	software_version = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		pass

	@staticmethod
	def dump(post):

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
			config[jsonkey] = json.loads(serializers.serialize('json', model.objects.all(), ensure_ascii=False))

		return config

#
# Forms
#

class JsonImportForm(forms.ModelForm):

	class Meta:
		model = JsonImport
		exclude = []

class JsonExportForm(forms.ModelForm):

	class Meta:
		model = JsonExport
		exclude = []

