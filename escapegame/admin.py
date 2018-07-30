from django.contrib import admin
from .models import EscapeGame, EscapeGameRoom, EscapeGameChallenge

class EscapeGameAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'video_path' )

class EscapeGameRoomAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'door_pin' )

class EscapeGameChallengeAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'room', 'solved' )

admin.site.register(EscapeGame, EscapeGameAdmin)
admin.site.register(EscapeGameRoom, EscapeGameRoomAdmin)
admin.site.register(EscapeGameChallenge, EscapeGameChallengeAdmin)
