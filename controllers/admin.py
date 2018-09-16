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
		action_pin = self.cleaned_data['action_pin']

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
		'protocol',
		'hostname',
		'port',
		'online',
	]
	fieldsets = (
		('Raspberry Pi', { 'fields': (
			'name',
			'slug',
			'protocol',
			'hostname',
			'port',
			'online',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'online' )

class GPIOAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'controller',
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
		'challenge',
		'solved',
		'solved_at',
	]

	fieldsets = GPIOAdmin.fieldsets + (

		('Challenge GPIO', { 'fields': (
			'challenge'
			'solved',
			'solved_at',
		)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return super(ChallengeGPIOAdmin, self).get_readonly_fields(request, obj) + ( 'solved_at', )

class CubeGPIOAdmin(ChallengeGPIOAdmin):

	form = CubeGPIOForm

	list_display = ChallengeGPIOAdmin.list_display + [
		'game',
		'tag_id',
		'taken_at',
		'placed_at',
	]

	fieldsets = ChallengeGPIOAdmin.fieldsets + (

		('Cube GPIO', { 'fields': (
			'game',
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
		'game',
		'room',
		'locked',
		'unlocked_at',
	]

	fieldsets = GPIOAdmin.fieldsets + (

		('Door GPIO', { 'fields': (
			'game',
			'room',
			'locked',
			'unlocked_at',
		)}),
	)

	def clean(self):

		game = self.cleaned_data['reset_pin']
		room = self.cleaned_data['reset_url']

		if game is None and room is None:
			raise ValidationError({
				'game': 'You have to supply at least one of \'Game\' or \'Room\'',
				'room': '',
			})

		if game is not None and room is not None:
			raise ValidationError({
				'game': 'Only one of \'Game\' or \'Room\' can be supplied',
				'room': '',
			})

	def get_readonly_fields(self, request, obj=None):
		return super(DoorGPIOAdmin, self).get_readonly_fields(request, obj) + ( 'unlocked_at', )

# Register our models to our custom admin site
site.register(ArduinoSketch, ArduinoSketchAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
site.register(ChallengeGPIO, ChallengeGPIOAdmin)
site.register(CubeGPIO, CubeGPIOAdmin)
site.register(DoorGPIO, DoorGPIOAdmin)
