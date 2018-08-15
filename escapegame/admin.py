# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse

from jsonexport.views import json_index_view, json_import_view, json_export_view

from .models import *

from collections import OrderedDict

from datetime import datetime

import json

# Escape game admin classes

class EscapeGameAdmin(admin.ModelAdmin):
	prepoluated_fields = { 'slug': ( 'escapegame_name', )}
	list_display = [
		'escapegame_name',
		'slug',
		'raspberrypi',
		'video_brief',
		'sas_door_pin',
		'corridor_door_pin',
		'sas_door_locked',
		'corridor_door_locked',
	]
	fieldsets = (
		('General', { 'fields': (
			'escapegame_name',
			'slug',
			'raspberrypi',
			'video_brief',
			)}),
		('Door controls', { 'fields': (
			'sas_door_pin',
			'corridor_door_pin',
			'sas_door_locked',
			'corridor_door_locked',
			)}),
		('Maps', { 'fields': (
			'map_image_path',
			'sas_door_image_path',
			'corridor_door_image_path',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'sas_door_locked', 'corridor_door_locked' )

class EscapeGameRoomAdmin(admin.ModelAdmin):
	prepoluated_fields = { 'slug': ( 'room_name', )}
	list_display = [
		'room_name',
		'slug',
		'escapegame',
		'raspberrypi',
		'door_pin',
		'door_locked',
	]
	fieldsets = (
		('General', { 'fields': (
			'room_name',
			'slug',
			'escapegame',
			'raspberrypi',
			)}),
		('Door controls', { 'fields': (
			'door_pin',
			'door_locked',
			)}),
		('Maps', { 'fields': (
			'room_image_path',
			'door_image_path',
			)})
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'door_locked' )

class EscapeGameChallengeAdmin(admin.ModelAdmin):
	list_display = ( 'challenge_name', 'slug', 'room', 'challenge_pin', 'solved' )
	prepoluated_fields = { 'slug': ( 'challenge_name', )}
	fieldset = (
		('General', { 'fields': (
			'challenge_name',
			'slug',
			'room',
			'challenge_pin',
			)}),
		('Status', { 'fields': (
			'solved',
			)}),
		('Maps', { 'fields': (
			'challenge_image_path',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'solved' )


# Register admin site

class EscapeGameAdminSite(admin.sites.AdminSite):

	index_template = 'admin/escapegame/index.html'

	"""
		Method to retrieve a model by its name
	"""
	def get_model_by_name(self, name, models):
		for model in models:
			if name == model['object_name']:
				return model
		return None

	"""
		Method to sort models according to different rules depending on the application
	"""
	def prepare_app_dict(self, app_dict):

		if 'app_label' not in app_dict:
			import pprint
			pp = pprint.PrettyPrinter()
			pp.pprint(app_dict)
			return app_dict

		app = app_dict['app_label']
		models = app_dict['models']

		# Sort the models by name
		models.sort(key=lambda x: x['name'])

		# For app escapegame, we want the models in reverse order
		if app == 'escapegame':
			app_dict['models'] = reversed(models)

		# For app controllers, we want a specific order for the models
		elif app == 'controllers':
			new_models = []
			for model in [ 'RaspberryPi', 'RemoteDoorPin', 'RemoteChallengePin', 'RemoteLedPin' ]:
				new_models.append(self.get_model_by_name(model, models))

			app_dict['models'] = new_models

		# For app jsonexport, we want to change the 'jsonexport' URL part to simply 'json'
		elif app == 'jsonexport':
			app_dict['app_url'] = app_dict['app_url'].replace('jsonexport', 'json')
			for model in models:
				model['admin_url'] = model['admin_url'].replace('jsonexport', 'json')

		return app_dict

	"""
		Method to sort all applications and models according to different rules depending on the application
	"""
	def prepare_apps_dict(self, app_dict):

		# Create new ordered dictionary to replace app dictionary
		ordered_dict = OrderedDict()

		# Fix app order
		for app in [ 'constance', 'jsonexport', 'multimedia', 'escapegame', 'controllers' ]:
			if app in app_dict:
				ordered_dict[app] = app_dict[app]

		# Replace app dictionary with our ordered dictionary
		if ordered_dict:
			app_dict = ordered_dict

		# Apply specific modifications to each app
		for app in app_dict:
			self.prepare_app_dict(app_dict[app])

		return app_dict

	"""
		Overrides `get_urls` to add our JSON import/export URLs.

		Method: AdminSite.get_urls(self)
		File: django/contrib/admin/sites.py
	"""
	def get_urls(self):
		from django.urls import path

		return super().get_urls() + [
			path('json/', json_index_view),
			path('json/import/', json_import_view),
			path('json/export/', json_export_view),
		]

	"""
		Overrides `get_app_list` so we can sort the app list to our liking on the main index page.

		Method: AdminSite.get_app_list(self, request)
		File: django/contrib/admin/sites.py
	"""
	def get_app_list(self, request):

		# Create app dictionary
		app_dict = self._build_app_dict(request)

		if 'app_label' in app_dict:
			self.prepare_app_dict(app_dict)
		else:
			app_dict = self.prepare_apps_dict(app_dict)

		#import pprint
		#pp = pprint.PrettyPrinter()
		#pp.pprint(app_dict)

		return app_dict.values()

	"""
		Overrides `app_index` so we can sort the model list to our liking on the application index page.

		Method: app_index(self, request, app_label, extra_context=None)
		File: django/contrib/admin/sites.py
	"""
	def app_index(self, request, app_label, extra_context=None):
		app_dict = self._build_app_dict(request, app_label)
		if not app_dict:
			raise Http404('The requested admin page does not exist.')
		# Sort the models alphabetically within each app.
		self.prepare_app_dict(app_dict)
		app_name = apps.get_app_config(app_label).verbose_name
		context = dict(
			self.each_context(request),
			title='%s administration' % app_name,
			app_list=[app_dict],
			app_label=app_label,
		)
		context.update(extra_context or {})

		request.current_app = self.name

		return TemplateResponse(request, self.app_index_template or [
			'admin/%s/app_index.html' % app_label,
			'admin/app_index.html'
		], context)


# Register all admin classes to our custom admin site

site = EscapeGameAdminSite(name='escapegame')

site.register(EscapeGame, EscapeGameAdmin)
site.register(EscapeGameRoom, EscapeGameRoomAdmin)
site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)

# Import Constance into our custom admin site
from constance.admin import Config as ConstanceConfig, ConstanceAdmin
site.register([ConstanceConfig], ConstanceAdmin)
admin.site.unregister([ConstanceConfig])
