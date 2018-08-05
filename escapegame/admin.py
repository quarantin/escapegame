# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

class ImageAdmin(admin.ModelAdmin):
	list_display = ( 'image_type', 'image_path' )

class VideoAdmin(admin.ModelAdmin):
	list_display = ( 'video_name', 'video_path' )

class RemotePinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'pin_type', 'pin_number', 'raspberrypi', 'callback_url' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'pin_type',
			'pin_number',
			'raspberrypi',
			'callback_url',
			)}),
	)

class RaspberryPiAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'hostname', 'port' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'hostname',
			'port',
			)}),
	)

class EscapeGameAdmin(admin.ModelAdmin):
	list_display = ( 'escape_game_name', 'video_brief' )
	prepoluated_fields = { 'slug': ( 'escape_game_name', )}
	fieldsets = (
		('General', { 'fields': (
			'escape_game_name',
			'escape_game_controller',
			'video_brief',
			)}),
		('Door controls', { 'fields': (
			'sas_door_pin',
			'corridor_door_pin',
			'sas_door_locked',
			'corridor_door_locked',
			)}),
		('Maps', { 'fields': (
			'map_image_path',
			'sas_door_image_path',
			'corridor_door_image_path',
			)}),
	)

class EscapeGameRoomAdmin(admin.ModelAdmin):
	list_display = ( 'room_name', 'door_pin' )
	prepoluated_fields = { 'slug': ( 'room_name', )}
	fieldsets = (
		('General', { 'fields': (
			'room_name',
			'room_controller',
			'escape_game',
			)}),
		('Door controls', { 'fields': (
			'door_pin',
			'door_locked',
			)}),
		('Maps', { 'fields': (
			'room_image_path',
			'door_image_path',
			)})
	)

class EscapeGameChallengeAdmin(admin.ModelAdmin):
	list_display = ( 'challenge_name', 'room', 'solved' )
	prepoluated_fields = { 'slug': ( 'challenge_name', )}
	fieldset = (
		('General', { 'fields': (
			'challenge_name',
			'room',
			)}),
		('Status', { 'fields': (
			'solved',
			)}),
		('General', { 'fields': (
			'challenge_image_path',
			)}),
	)

admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(RemotePin, RemotePinAdmin)
admin.site.register(RaspberryPi, RaspberryPiAdmin)
admin.site.register(EscapeGame, EscapeGameAdmin)
admin.site.register(EscapeGameRoom, EscapeGameRoomAdmin)
admin.site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)
