# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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

		reset_pin = 'reset_pin' in self.cleaned_data and self.cleaned_data['reset_pin'] or None
		reset_url = 'reset_url' in self.cleaned_data and self.cleaned_data['reset_url'] or None
		action_pin = 'action_pin' in self.cleaned_data and self.cleaned_data['action_pin'] or None
		action_url = 'action_url' in self.cleaned_data and self.cleaned_data['action_url'] or None

		if reset_pin is not None and not libraspi.is_valid_pin(reset_pin):
			raise ValidationError({
				'reset_pin': _('Pin number %d is not a valid GPIO on a Raspberry Pi v3') % reset_pin,
			})

		if action_pin is not None and not libraspi.is_valid_pin(action_pin):
			raise ValidationError({
				'action_pin': _('Pin number %d is not a valid GPIO on a Raspberry Pi v3') % action_pin,
			})

		if action_pin is not None and action_url is not None:
			raise ValidationError({
				'action_pin': _('You can only specify an action pin, or an action URL, but not both'),
				'action_url': '',
			})

		if reset_pin is not None and reset_url is not None:
			raise ValidationError({
				'reset_pin': _('You can only specify a reset pin, or a reset URL, but not both'),
				'reset_url': '',
			})

		return self.cleaned_data

class ChallengeGPIOForm(GPIOForm):

	class Meta:
		model = ChallengeGPIO
		exclude = []

	def clean(self):

		super(ChallengeGPIOForm, self).clean()

		cube = 'cube' in self.cleaned_data and self.cleaned_data['cube'] or None
		chall_type = 'challenge_type' in self.cleaned_data and self.cleaned_data['challenge_type'] or None

		if chall_type != ChallengeGPIO.TYPE_DEFAULT and cube is None:
			raise ValidationError({
				'cube': _('Cube field cannot be empty for cube challenges'),
			})

class DoorGPIOForm(GPIOForm):

	class Meta:
		model = DoorGPIO
		exclude = []

	def clean(self):

		super(DoorGPIOForm, self).clean()

		has_dependency = 'dependent_on' in self.cleaned_data and self.cleaned_data['dependent_on'] is not None

		if has_dependency:

			from escapegame.models import EscapeGameRoom

			try:
				room = EscapeGameRoom.objects.get(door=self.instance)

				raise ValidationError({
					'dependent_on': _('You cannot create a dependency for this door GPIO because it is already assigned to room `%s`.\nIf you really want to create a dependency for this door GPIO, please unassign it from the room first.' % room.name),
				})

			except EscapeGameRoom.DoesNotExist:
				pass

class LiftGPIOForm(forms.ModelForm):

	class Meta:
		model = LiftGPIO
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
		'media_type',
		'protocol',
		'hostname',
		'port',
		'online',
	]
	fieldsets = (
		('Raspberry Pi', { 'fields': (
			'name',
			'slug',
			'media_type',
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
		)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )

class ChallengeGPIOAdmin(GPIOAdmin):

	form = ChallengeGPIOForm

	list_display = GPIOAdmin.list_display + [
		'challenge_type',
		'cube',
		'solved',
		'solved_at',
	]

	fieldsets = (

		('Challenge GPIO', { 'fields': (
			'name',
			'slug',
			'controller',
		)}),

		('Challenge', { 'fields': (
			'challenge_type',
			'cube',
			'solved',
			'solved_at',
		)}),

	) + GPIOAdmin.fieldsets

	def get_readonly_fields(self, request, obj=None):
		return super(ChallengeGPIOAdmin, self).get_readonly_fields(request, obj) + ( 'solved', 'solved_at' )

class DoorGPIOAdmin(GPIOAdmin):

	form = DoorGPIOForm

	list_display = GPIOAdmin.list_display + [
		'dependent_on',
		'locked',
		'unlocked_at',
	]

	fieldsets = (

		('Door GPIO', { 'fields': (
			'name',
			'slug',
			'controller',
		)}),

		('Door', { 'fields': (
			'dependent_on',
			'locked',
			'unlocked_at',
		)}),

	) + GPIOAdmin.fieldsets

	def get_readonly_fields(self, request, obj=None):
		return super(DoorGPIOAdmin, self).get_readonly_fields(request, obj) + ( 'locked', 'unlocked_at' )

class LiftGPIOAdmin(admin.ModelAdmin):

	form = LiftGPIOForm

	list_display = [
		'name',
		'slug',
		'controller',
		'game',
		'briefing_video',
		'pin',
		'raised',
		'image',
	]

	fieldsets = (

		('Lift GPIO', { 'fields': (
			'name',
			'slug',
			'controller',
		)}),

		('Lift', { 'fields': (
			'game',
			'briefing_video',
			'pin',
			'raised',
		)}),

		('Multimedia', { 'fields': (
			'image',
		)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )

# Register our models to our custom admin site
site.register(ArduinoSketch, ArduinoSketchAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
site.register(ChallengeGPIO, ChallengeGPIOAdmin)
site.register(DoorGPIO, DoorGPIOAdmin)
site.register(LiftGPIO, LiftGPIOAdmin)
