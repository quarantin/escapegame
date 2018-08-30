from django.contrib import admin

from escapegame.admin import site

from .models import *

# Controllers admin classes

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
	list_display = ( 'name', 'challenge', 'raspberrypi', 'url_callback_validate', 'url_callback_reset' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'challenge',
			'raspberrypi',
			'url_callback_validate',
			'url_callback_reset',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_callback_validate', 'url_callback_reset' )

class RemoteDoorPinAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'room', 'raspberrypi', 'url_callback_lock', 'url_callback_unlock' )
	fieldsets = (
		('General', { 'fields': (
			'name',
			'room',
			'raspberrypi',
			'url_callback_lock',
			'url_callback_unlock',
			)}),
	)

	def get_readonly_fields(self, request, obj=None):
		return self.readonly_fields + ( 'url_callback_lock', 'url_callback_unlock' )


site.register(RaspberryPi, RaspberryPiAdmin)
site.register(RemoteChallengePin, RemoteChallengePinAdmin)
site.register(RemoteDoorPin, RemoteDoorPinAdmin)
