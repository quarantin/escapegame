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
		'hostname',
		'port',
	]

class ChallengeAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'raspberrypi',
		'pin',
		'solved',
		'solved_at',
	]

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'solved_at', )

class CubeAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'raspberrypi',
		'pin',
		'tag_id',
		'taken_at',
		'placed_at',
	]

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'taken_at', 'placed_at' )

class DoorAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'raspberrypi',
		'pin',
		'locked',
		'unlocked_at',
	]

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'unlocked_at', )

# Register our models to our custom admin site
site.register(ArduinoSketch, ArduinoSketchAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
site.register(Challenge, ChallengeAdmin)
site.register(Cube, CubeAdmin)
site.register(Door, DoorAdmin)
