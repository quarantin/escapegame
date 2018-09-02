# -*- coding: utf-8 -*-

from django.contrib import admin

from escapegame.admin import site

from .models import *


# Media admin classes

class ImageAdmin(admin.ModelAdmin):
	list_display = [
		'image_name',
		'image_path',
		'width',
		'height',
	]

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'width', 'height' )

class VideoAdmin(admin.ModelAdmin):
	list_display = [
		'slug',
		'video_name',
		'video_path',
	]

site.register(Image, ImageAdmin)
site.register(Video, VideoAdmin)
