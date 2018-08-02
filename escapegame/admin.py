# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import EscapeGame, EscapeGameRoom, EscapeGameChallenge

class EscapeGameAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'video_path' )
	prepoluated_fields = { 'slug': ('name',) }

class EscapeGameRoomAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'door_pin' )
	prepoluated_fields = { 'slug': ('name',) }

class EscapeGameChallengeAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'room', 'solved' )
	prepoluated_fields = { 'slug': ('name',) }

admin.site.register(EscapeGame, EscapeGameAdmin)
admin.site.register(EscapeGameRoom, EscapeGameRoomAdmin)
admin.site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)
