# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin

from escapegame.admin import site

from .models import *


#
# Forms
#

class GPIOForm(forms.ModelForm):

	class Meta:
		model = GPIO
		exclude = []

	def clean(self):

		reset_pin = self.cleaned_data['reset_pin']
		reset_url = self.cleaned_data['reset_url']

		action_pin = self.cleaned_data['action_pin']
		action_url = self.cleaned_data['action_url']

		if reset_pin is None and reset_url is None:
			raise ValidationError({
				'reset_pin': 'You have to supply at least one of \'Reset PIN\' or \'Reset URL\'',
				'reset_url': '',
			})

		if action_pin is None and action_url is None:
			raise ValidationError({
				'action_pin': 'You have to supply at least one of \'Action PIN\' or \'Action URL\'',
				'action_url': '',
			})

		if reset_pin is not None and reset_url is not None:
			raise ValidationError({
				'reset_pin': 'Only one of \'Reset PIN\' or \'Reset URL\' can be supplied',
				'reset_url': '',
			})

		if action_pin is not None and action_url is not None:
			raise ValidationError({
				'action_pin': 'Only one of \'Reset PIN\' or \'Reset URL\' can be supplied',
				'action_url': '',
			})

		if reset_pin is not None and not libraspi.is_valid_pin(reset_pin):
			raise ValidationError({
				'reset_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % reset_pin,
			})

		if action_pin is not None and not libraspi.is_valid_pin(action_pin):
			raise ValidationError({
				'action_pin': 'PIN number %d is not a valid GPIO on a Raspberry Pi v3' % action_pin,
			})

		return self.cleaned_data

class ChallengeGPIOForm(GPIOForm):

	class Meta:
		model = ChallengeGPIO
		exclude = []

class CubeGPIOForm(GPIOForm):

	class Meta:
		model = CubeGPIO
		exclude = []

class DoorGPIOForm(GPIOForm):

	class Meta:
		model = DoorGPIO
		exclude = []

#
# Controllers admin classes
#

class ArduinoSketchAdmin(admin.ModelAdmin):
	list_display = [
		'sketch_name',
		'sketch_path',
	]

	def get_readonly_fields(self, request, obj=None):
		field = 'sketch_path'
		if not obj or not obj.sketch_code:
			field = 'sketch_code'

		return self.readonly_fields + ( field, )

class RaspberryPiAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'hostname',
		'port',
	]
	fieldsets = (
		('Raspberry Pi', { 'fields': (
			'name',
			'slug',
			'hostname',
			'port',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )

class GPIOAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'controller',
		#'parent',
		'action_pin',
		'reset_pin',
		'action_url',
		'reset_url',
		'image',
	]
	fieldsets = (
		('GPIO', { 'fields': (
			'name',
			'slug',
			'controller',
			#'parent',
		)}),

		('Action configuration', { 'fields': (
			'action_pin',
			'action_url',
		)}),

		('Reset configuration', { 'fields': (
			'reset_pin',
			'reset_url',
		)}),

		('Multimedia', { 'fields': (
			'image',
		)})
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )

class ChallengeGPIOAdmin(GPIOAdmin):

	form = ChallengeGPIOForm

	list_display = GPIOAdmin.list_display + [
		'solved',
		'solved_at',
	]

	fieldsets = GPIOAdmin.fieldsets + (

		('Challenge GPIO', { 'fields': (
			'solved',
			'solved_at',
		)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return super(ChallengeGPIOAdmin, self).get_readonly_fields(request, obj) + ( 'solved_at', )

class CubeGPIOAdmin(GPIOAdmin):

	form = CubeGPIOForm

	list_display = GPIOAdmin.list_display + [
		'tag_id',
		'taken_at',
		'placed_at',
	]

	fieldsets = GPIOAdmin.fieldsets + (

		('Cube GPIO', { 'fields': (
			'tag_id',
			'taken_at',
			'placed_at',
		)}),

	)

	def get_readonly_fields(self, request, obj=None):
		return super(CubeGPIOAdmin, self).get_readonly_fields(request, obj) + ( 'taken_at', 'placed_at' )

class DoorGPIOAdmin(GPIOAdmin):

	form = DoorGPIOForm

	list_display = GPIOAdmin.list_display + [
		'locked',
		'unlocked_at',
	]

	fieldsets = GPIOAdmin.fieldsets + (

		('Door GPIO', { 'fields': (
			'locked',
			'unlocked_at',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return super(DoorGPIOAdmin, self).get_readonly_fields(request, obj) + ( 'unlocked_at', )

# Register our models to our custom admin site
site.register(ArduinoSketch, ArduinoSketchAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
site.register(ChallengeGPIO, ChallengeGPIOAdmin)
site.register(CubeGPIO, CubeGPIOAdmin)
site.register(DoorGPIO, DoorGPIOAdmin)
