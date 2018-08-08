# -*- coding: utf-8 -*-

import json
import pprint
from django.contrib.admin import site
from import_export import admin, resources
from .models import *


# Media resources

class ImageResource(resources.ModelResource):
	class Meta:
		model = Image

class VideoResource(resources.ModelResource):
	class Meta:
		model = Video


# Escape game resources

class EscapeGameResource(resources.ModelResource):
	class Meta:
		model = EscapeGame

class EscapeGameRoomResource(resources.ModelResource):
	class Meta:
		model = EscapeGameRoom

class EscapeGameChallengeResource(resources.ModelResource):
	class Meta:
		model = EscapeGameChallenge


# Remote pin resources

class RaspberryPiResource(resources.ModelResource):
	class Meta:
		model = RaspberryPi

class RemoteChallengePinResource(resources.ModelResource):
	class Meta:
		model = RemoteChallengePin

class RemoteDoorPinResource(resources.ModelResource):
	class Meta:
		model = RemoteDoorPin

class RemoteLedPinResource(resources.ModelResource):
	class Meta:
		model = RemoteLedPin


# Media admin classes

class ImageAdmin(admin.ImportExportActionModelAdmin):
	resource_class = ImageResource
	list_display = ( 'image_type', 'image_path' )

class VideoAdmin(admin.ImportExportActionModelAdmin):
	resource_class = VideoResource
	list_display = ( 'video_name', 'video_path' )


# Escape game admin classes

class EscapeGameAdmin(admin.ImportExportActionModelAdmin):
	resource_class = EscapeGameResource
	list_display = [ 'escape_game_name', 'video_brief', 'slug' ]
	prepoluated_fields = { 'slug': ( 'escape_game_name', )}
	fieldsets = (
		('General', { 'fields': (
			'escape_game_name',
			'slug',
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

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'sas_door_locked', 'corridor_door_locked' )

class EscapeGameRoomAdmin(admin.ImportExportActionModelAdmin):
	resource_class = EscapeGameRoomResource
	list_display = ( 'room_name', 'door_pin' )
	prepoluated_fields = { 'slug': ( 'room_name', )}
	fieldsets = (
		('General', { 'fields': (
			'room_name',
			'slug',
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

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'door_locked' )

class EscapeGameChallengeAdmin(admin.ImportExportActionModelAdmin):
	resource_class = EscapeGameChallengeResource
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
		('General', { 'fields': (
			'challenge_image_path',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'slug', 'solved' )


# Remote pin admin classes

class RaspberryPiAdmin(admin.ImportExportActionModelAdmin):
	resource_class = RaspberryPiResource
	list_display = ( 'name', 'hostname', 'port' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'hostname',
			'port',
			)}),
	)

class RemoteChallengePinAdmin(admin.ImportExportActionModelAdmin):
	resource_class = RemoteChallengePinResource
	list_display = ( 'name', 'challenge', 'pin_number', 'raspberrypi', 'callback_url_validate', 'callback_url_reset' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'challenge',
			'raspberrypi',
			'pin_number',
			'callback_url_validate',
			'callback_url_reset',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'callback_url_validate', 'callback_url_reset' )

class RemoteDoorPinAdmin(admin.ImportExportActionModelAdmin):
	resource_class = RemoteDoorPinResource
	list_display = ( 'name', 'room', 'pin_number', 'raspberrypi', 'callback_url_lock', 'callback_url_unlock' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'room',
			'raspberrypi',
			'pin_number',
			'callback_url_lock',
			'callback_url_unlock',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'callback_url_lock', 'callback_url_unlock' )

class RemoteLedPinAdmin(admin.ImportExportActionModelAdmin):
	resource_class = RemoteLedPinResource
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

site.register(Image, ImageAdmin)
site.register(Video, VideoAdmin)
site.register(RemoteChallengePin, RemoteChallengePinAdmin)
site.register(RemoteDoorPin, RemoteDoorPinAdmin)
site.register(RemoteLedPin, RemoteLedPinAdmin)
site.register(RaspberryPi, RaspberryPiAdmin)
site.register(EscapeGame, EscapeGameAdmin)
site.register(EscapeGameRoom, EscapeGameRoomAdmin)
site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)
