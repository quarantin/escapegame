from django.conf import settings
from django.http import JsonResponse

from .models import VideoPlayer

import os, subprocess

def get_video_player():

	video_players = VideoPlayer.objects.all()
	for video_player in video_players:
		player = str(video_player)
		if os.path.exists(player):
			return player

	raise Exception('No video player found.')

def play_video(request, filename):

	try:
		video_player = get_video_player()
		video_path = os.path.join(settings.VIDEO_PATH, filename)

		subprocess.call([ video_player, video_path ])

		return JsonResponse({
			'status': 'OK',
			'message': 'Success.',
		})

	except Exception as err:
		return JsonResponse({
			'status': 'KO',
			'message': 'An error has occured: %s' % err,
		})

def stop_video(request):

	try:
		video_player = get_video_player()

		subprocess.call([ 'killall', video_player ])

		return JsonResponse({
			'status': 'OK',
			'message': 'Success.',
		})

	except Exception as err:
		return JsonResponse({
			'status': 'KO',
			'message': 'An error has occured: %s' % err,
		})
