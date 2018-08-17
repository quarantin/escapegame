from django.contrib import admin

from escapegame.admin import site

from .models import *

# Media admin classes

class ImageAdmin(admin.ModelAdmin):
	list_display = [
		'image_name',
		'image_path',
	]

class VideoAdmin(admin.ModelAdmin):
	list_display = [
		'video_name',
		'video_path',
	]

class VideoPlayerAdmin(admin.ModelAdmin):
	list_display = [
		'video_player_name',
		'video_player_path',
	]

site.register(Image, ImageAdmin)
site.register(Video, VideoAdmin)
