from django.contrib import admin
from .models import VideoPlayer

class VideoPlayerConfig(admin.ModelAdmin):
	list_display = [ 'video_player' ]

admin.site.register(VideoPlayer, VideoPlayerConfig)
