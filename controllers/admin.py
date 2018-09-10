# -*- coding: utf-8 -*-

from django.contrib import admin

from escapegame.admin import site

from .models import *


# Controllers admin classes

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

class ChallengeGPIOAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'controller',
		'reset_pin',
		'action_pin',
		'reset_url',
		'action_url',
		'solved',
		'solved_at',
	]
	fieldsets = (
		('Challenge GPIO', { 'fields': (
			'name',
			'slug',
			'controller',
			'reset_pin',
			'action_pin',
			'reset_url',
			'action_url',
			'solved',
			'solved_at',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'solved_at' )

class CubeGPIOAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'controller',
		'reset_pin',
		'action_pin',
		'reset_url',
		'action_url',
		'tag_id',
		'taken_at',
		'placed_at',
	]
	fieldsets = (
		('Cube GPIO', { 'fields': (
			'name',
			'slug',
			'controller',
			'reset_pin',
			'action_pin',
			'reset_url',
			'action_url',
			'tag_id',
			'taken_at',
			'placed_at',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'taken_at', 'placed_at' )

class DoorGPIOAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'controller',
		'reset_pin',
		'action_pin',
		'reset_url',
		'action_url',
		'locked',
		'unlocked_at',
	]
	fieldsets = (
		('Door GPIO', { 'fields': (
			'name',
			'slug',
			'controller',
			'reset_pin',
			'action_pin',
			'reset_url',
			'action_url',
			'locked',
			'unlocked_at',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'unlocked_at' )

# Register our models to our custom admin site
site.register(ArduinoSketch, ArduinoSketchAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
site.register(ChallengeGPIO, ChallengeGPIOAdmin)
site.register(CubeGPIO, CubeGPIOAdmin)
site.register(DoorGPIO, DoorGPIOAdmin)
