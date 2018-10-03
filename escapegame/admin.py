# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TimeInput, DateTimeInput
from django import forms
from django.db import models
from django.apps import apps
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse

from .models import *

from collections import OrderedDict

from datetime import datetime

import json
import re


# Escape game admin classes

class EscapeGameAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.DurationField: { 'widget': DateTimeInput },
	}
	list_display = [
		'name',
		'slug',
		'time_limit',
		'controller',
		'map_image',
	]
	fieldsets = (
		('Escape Game', { 'fields': (
			'name',
			'slug',
			'time_limit',
			'controller',
			)}),
		('Map', { 'fields': (
			'map_image',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )

class EscapeGameCubeForm(forms.ModelForm):

	class Meta:
		model = EscapeGameCube
		fields = [ 'tag_id' ]

	def clean(self):

		if 'tag_id' not in self.cleaned_data:
			return

		tag_id = self.cleaned_data['tag_id']
		match = re.search('^[0-9A-F]{8}$', tag_id) is not None
		if not match:
			raise ValidationError({
				'tag_id': _('Invalid format for tag ID, must contain 8 hexadecimal digits (for example: `FF010203`)'),
			})

class EscapeGameCubeAdmin(admin.ModelAdmin):
	form = EscapeGameCubeForm
	list_display = [
		'name',
		'game',
		'tag_id',
		'cube_delay',
		'briefing_media',
		'losers_media',
		'winners_media',
	]
	fieldsets = (
		('Escape Game Cube', { 'fields': (
			'name',
			'game',
			'tag_id',
			'cube_delay',
		)}),

		('Multimedia Files', { 'fields': (
			'briefing_media',
			'losers_media',
			'winners_media',
		)}),
	)

class EscapeGameRoomForm(forms.ModelForm):

	class Meta:
		model = EscapeGameRoom
		fields = [
			'door'
		]

	def clean(self):

		if 'door' not in self.cleaned_data:
			return

		door = self.cleaned_data['door']

		try:
			gpio = DoorGPIO.objects.get(pk=door.pk)
			if gpio.dependent_on is not None:
				raise ValidationError({
					'door': _('You cannot assign this DoorGPIO because it has a dependency to challenge `%s`.\nIf you really want to assign this DoorGPIO, please remove its dependency first.' % gpio.dependent_on.name),
				})

		except DoorGPIO.DoesNotExist:
			pass

class EscapeGameRoomAdmin(admin.ModelAdmin):
	form = EscapeGameRoomForm
	list_display = [
		'name',
		'slug',
		'game',
		'controller',
		'starts_the_timer',
		'stops_the_timer',
		'door',
		'room_image',
		'door_image',
	]
	fieldsets = (
		('Escape Game Room', { 'fields': (
			'name',
			'slug',
			'game',
			'controller',
			'starts_the_timer',
			'stops_the_timer',
			)}),
		('Door controls', { 'fields': (
			'door',
			)}),
		('Map', { 'fields': (
			'room_image',
			'door_image',
			)})
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'unlock_time' )

class EscapeGameChallengeAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'room',
		'gpio',
		'dependent_on',
		'solved_media',
		'challenge_image',
		'challenge_solved_image',
		'callback_url_solve',
		'callback_url_reset',
	]
	fieldsets = (
		('Escape Game Challenge', { 'fields': (
			'name',
			'slug',
			'room',
			'dependent_on',
			)}),
		('Challenge Controls', { 'fields': (
			'gpio',
			)}),
		('Multimedia Files', { 'fields': (
			'solved_media',
			)}),
		('Map', { 'fields': (
			'challenge_image',
			'challenge_solved_image',
			)}),
		('URLs', { 'fields': (
			'callback_url_solve',
			'callback_url_reset',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'solved_time', 'callback_url_solve', 'callback_url_reset' )


# Our custom admin site

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
			app_dict['models'] = models

		# For app jsonexport, we want the models in reverse order,
		# and we want to change the 'jsonexport' URL part to simply 'json'
		elif app == 'jsonexport':
			app_dict['models'] = reversed(models)
			app_dict['app_url'] = app_dict['app_url'].replace('jsonexport', 'json')
			for model in models:
				if 'admin_url' in model:
					model['admin_url'] = model['admin_url'].replace('jsonexport/jsonexport', 'json/export')
					model['admin_url'] = model['admin_url'].replace('jsonexport/jsonimport', 'json/import')

		return app_dict

	"""
		Method to sort all applications and models according to different rules depending on the application
	"""
	def prepare_app_list_dict(self, app_dict):

		# Create new ordered dictionary to replace app dictionary
		ordered_dict = OrderedDict()

		# Fix app order
		for app in [ 'jsonexport', 'multimedia', 'escapegame', 'controllers' ]:
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
		Overrides `get_app_list` so we can sort the app list to our liking on the main index page.

		Method: AdminSite.get_app_list(self, request)
		File: django/contrib/admin/sites.py
	"""
	def get_app_list(self, request):

		# Create app dictionary
		app_dict = self._build_app_dict(request)

		if 'app_label' in app_dict:
			app_dict = self.prepare_app_dict(app_dict)
		else:
			app_dict = self.prepare_app_list_dict(app_dict)

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
		app_dict = self.prepare_app_dict(app_dict)
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


# Instanciate our custom admin site
site = EscapeGameAdminSite(name='escapegame')

# Register our models to our custom admin site
site.register(EscapeGame, EscapeGameAdmin)
site.register(EscapeGameCube, EscapeGameCubeAdmin)
site.register(EscapeGameRoom, EscapeGameRoomAdmin)
site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)
