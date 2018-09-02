# -*- coding: utf-8 -*-

from django.contrib import admin

from escapegame.admin import site

from .models import ArduinoSketch, RaspberryPi


# Controllers admin classes

class ArduinoSketchAdmin(admin.ModelAdmin):
	list_display = ( 'sketch_name', 'sketch_path' )

	def get_readonly_fields(self, request, obj=None):
		field = 'sketch_path'
		if not obj or not obj.sketch_code:
			field = 'sketch_code'

		return self.readonly_fields + ( field, )

class RaspberryPiAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'hostname', 'port' )


# Register our models to our custom admin site
site.register(ArduinoSketch, ArduinoSketchAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
