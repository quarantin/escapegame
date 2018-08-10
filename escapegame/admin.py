# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from jsonexport.views import json_index_view, json_import_view, json_export_view

from .models import *

from collections import OrderedDict

from datetime import datetime

import json

# Escape game admin classes

class EscapeGameAdmin(admin.ModelAdmin):
	list_display = [ 'escapegame_name', 'video_brief', 'slug' ]
	prepoluated_fields = { 'slug': ( 'escapegame_name', )}
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
	list_display = ( 'room_name', 'door_pin' )
	prepoluated_fields = { 'slug': ( 'room_name', )}
	fieldsets = (
		('General', { 'fields': (
			'room_name',
			'slug',
			'raspberrypi',
			'escapegame',
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
	list_display = ( 'challenge_name', 'room', 'solved' )
	prepoluated_fields = { 'slug': ( 'challenge_name', )}
	fieldset = (
		('General', { 'fields': (
			'challenge_name',
			'slug',
			'room',
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


# Remote pin admin classes

class RaspberryPiAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'hostname', 'port' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'hostname',
			'port',
			)}),
	)

class RemoteChallengePinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'challenge', 'pin_number', 'raspberrypi', 'url_callback_validate', 'url_callback_reset' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'challenge',
			'raspberrypi',
			'pin_number',
			'url_callback_validate',
			'url_callback_reset',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_callback_validate', 'url_callback_reset' )

class RemoteDoorPinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'room', 'pin_number', 'raspberrypi', 'url_callback_lock', 'url_callback_unlock' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'room',
			'raspberrypi',
			'pin_number',
			'url_callback_lock',
			'url_callback_unlock',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_callback_lock', 'url_callback_unlock' )

class RemoteLedPinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'pin_number', 'raspberrypi', 'url_on', 'url_off' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'raspberrypi',
			'pin_number',
			'url_on',
			'url_off',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_on', 'url_off' )

# Register admin site

class EscapeGameAdminSite(admin.sites.AdminSite):

	index_template = 'admin/index.html'

	def get_urls(self):
		from django.urls import path

		urls = super().get_urls()
		urls += [
			path('json/', json_index_view),
			path('json/import/', json_import_view),
			path('json/export/', json_export_view),
		]
		return urls

	def get_model_by_name(self, model_list, name):
		for model in model_list:
			if name == model['object_name']:
				return model
		return None

	def get_app_list(self, request):
		import pprint
		pp = pprint.PrettyPrinter()
		app_dict = self._build_app_dict(request)

		for app in app_dict:
			if app == 'jsonexport':
				app_dict[app]['app_url'] = app_dict[app]['app_url'].replace('jsonexport', 'json')
				for model in app_dict[app]['models']:
					model['admin_url'] = model['admin_url'].replace('jsonexport', 'json')

		pp.pprint(app_dict)
		# Sort the apps alphabetically.
		app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

		# Invert order for the last two apps (escapegame and jsonexport)
		if len(app_list) > 1:
			tmp = app_list[-1]
			app_list[-1] = app_list[-2]
			app_list[-2] = tmp

		# Sort the models alphabetically within each app.
		for app in app_list:
			app['models'].sort(key=lambda x: x['name'])
			if app['name'] == 'Escapegame':

				new_models = []

				new_models.append(self.get_model_by_name(app['models'], 'Image'))
				new_models.append(self.get_model_by_name(app['models'], 'Video'))
				new_models.append(self.get_model_by_name(app['models'], 'EscapeGame'))
				new_models.append(self.get_model_by_name(app['models'], 'EscapeGameRoom'))
				new_models.append(self.get_model_by_name(app['models'], 'EscapeGameChallenge'))
				new_models.append(self.get_model_by_name(app['models'], 'RaspberryPi'))
				new_models.append(self.get_model_by_name(app['models'], 'RemoteChallengePin'))
				new_models.append(self.get_model_by_name(app['models'], 'RemoteDoorPin'))
				new_models.append(self.get_model_by_name(app['models'], 'RemoteLedPin'))

				app['models'] = new_models

			print("DEBUG app=%s models=%s" % (app, app['models']))

		return app_list


# Register all admin classes to our custom admin site

site = EscapeGameAdminSite(name='escapegame')

site.register(EscapeGame, EscapeGameAdmin)
site.register(EscapeGameRoom, EscapeGameRoomAdmin)
site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
site.register(RemoteChallengePin, RemoteChallengePinAdmin)
site.register(RemoteDoorPin, RemoteDoorPinAdmin)
site.register(RemoteLedPin, RemoteLedPinAdmin)

from constance.admin import Config as ConstanceConfig, ConstanceAdmin
site.register([ConstanceConfig], ConstanceAdmin)
admin.site.unregister([ConstanceConfig])
