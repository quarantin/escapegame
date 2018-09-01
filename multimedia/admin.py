from django.contrib import admin

from escapegame.admin import site

from .models import *


# Media admin classes

class ImageAdmin(admin.ModelAdmin):
	list_display = [
		'image_name',
		'image_path',
	]

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'width', 'height' )

class VideoAdmin(admin.ModelAdmin):
	list_display = [
		'video_name',
		'slug',
		'video_path',
		'raspberrypi',
	]
	fieldsets = (
		('General', { 'fields': (
			'video_name',
			'slug',
			'video_path',
			)}),
		('Remote controls', { 'fields': (
			'raspberrypi',
			)})
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', )

site.register(Image, ImageAdmin)
site.register(Video, VideoAdmin)
