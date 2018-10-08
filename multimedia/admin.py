# -*- coding: utf-8 -*-

from django import forms
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

class MultimediaFileForm(forms.ModelForm):
	class Meta:
		model = MultimediaFile
		exclude = []

class MultimediaFileAdmin(admin.ModelAdmin):
	form = MultimediaFileForm
	list_display = [
		'name',
		'slug',
		'game',
		'loop',
		'audio_out',
		'media_type',
		'path',
		'status',
	]
	fieldsets = (
		('Multimedia File', { 'fields': (
			'name',
			'slug',
			'game',
			'loop',
			'audio_out',
			'media_type',
			'path',
			'status',
		)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'status' )

# Register our models to our custom admin site
site.register(Image, ImageAdmin)
site.register(MultimediaFile, MultimediaFileAdmin)
