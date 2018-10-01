# -*- coding: utf-8 -*-

from django.contrib import admin

from escapegame.admin import site

from .models import *


# Media admin classes

class ImageAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'path',
		'width',
		'height',
	]

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'width', 'height' )

class VideoAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'path',
	]
	fieldsets = (
		('Video', { 'fields': (
			'name',
			'slug',
			'path',
		)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )

class AudioAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'path',
	]
	fieldsets = (
		('Audio', { 'fields': (
			'name',
			'slug',
			'path',
		)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )


# Register our models to our custom admin site
site.register(Image, ImageAdmin)
site.register(Video, VideoAdmin)
site.register(Audio, AudioAdmin)
