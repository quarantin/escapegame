# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import *

# Media admin classes

class ImageAdmin(admin.ModelAdmin):
	list_display = ( 'image_type', 'image_path' )

class VideoAdmin(admin.ModelAdmin):
	list_display = ( 'video_name', 'video_path' )


# Escape game admin classes

class EscapeGameAdmin(admin.ModelAdmin):
	list_display = [ 'escapegame_name', 'video_brief', 'slug' ]
	prepoluated_fields = { 'slug': ( 'escapegame_name', )}
	fieldsets = (
		('General', { 'fields': (
			'escapegame_name',
			'slug',
			'raspbberypi',
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

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'sas_door_locked', 'corridor_door_locked' )

class EscapeGameRoomAdmin(admin.ModelAdmin):
	list_display = ( 'room_name', 'door_pin' )
	prepoluated_fields = { 'slug': ( 'room_name', )}
	fieldsets = (
		('General', { 'fields': (
			'room_name',
			'slug',
			'raspberrypi',
			'escapegame',
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

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'door_locked' )

class EscapeGameChallengeAdmin(admin.ModelAdmin):
	list_display = ( 'challenge_name', 'room', 'solved' )
	prepoluated_fields = { 'slug': ( 'challenge_name', )}
	fieldset = (
		('General', { 'fields': (
			'challenge_name',
			'slug',
			'room',
			)}),
		('Status', { 'fields': (
			'solved',
			)}),
		('Maps', { 'fields': (
			'challenge_image_path',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'solved' )


# Remote pin admin classes

class RaspberryPiAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'hostname', 'port' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'hostname',
			'port',
			)}),
	)

class RemoteChallengePinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'challenge', 'pin_number', 'raspberrypi', 'url_callback_validate', 'url_callback_reset' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'challenge',
			'raspberrypi',
			'pin_number',
			'url_callback_validate',
			'url_callback_reset',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_callback_validate', 'url_callback_reset' )

class RemoteDoorPinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'room', 'pin_number', 'raspberrypi', 'url_callback_lock', 'url_callback_unlock' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'room',
			'raspberrypi',
			'pin_number',
			'url_callback_lock',
			'url_callback_unlock',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_callback_lock', 'url_callback_unlock' )

class RemoteLedPinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'pin_number', 'raspberrypi', 'url_on', 'url_off' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'raspberrypi',
			'pin_number',
			'url_on',
			'url_off',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_on', 'url_off' )


# Register all admin classes to django admin site

admin.site.register(Image, ImageAdmin)
admin.site.register(EscapeGame, EscapeGameAdmin)
admin.site.register(EscapeGameRoom, EscapeGameRoomAdmin)
admin.site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)
admin.site.register(RaspberryPi, RaspberryPiAdmin)
admin.site.register(RemoteChallengePin, RemoteChallengePinAdmin)
admin.site.register(RemoteDoorPin, RemoteDoorPinAdmin)
admin.site.register(RemoteLedPin, RemoteLedPinAdmin)
admin.site.register(Video, VideoAdmin)
