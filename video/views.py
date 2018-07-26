from django.conf import settings
from django.http import JsonResponse

import os, subprocess

def play_video(request, filename):

	try:
		video_path = os.path.join(settings.VIDEO_PATH, filename)
		subprocess.call([ settings.VIDEO_PLAYER, video_path ])
		return JsonResponse({ 'status': 'OK' })
	except:
		return JsonResponse({ 'status': 'KO' })

def stop_video(request):

	try:
		subprocess.call([ 'killall', settings.VIDEO_PLAYER ])
		return JsonResponse({ 'status': 'OK' })
	except:
		return JsonResponse({ 'status': 'KO' })
