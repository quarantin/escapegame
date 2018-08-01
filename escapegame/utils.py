import os, subprocess

#import RPi.GPIO as GPIO

from .models import VideoPlayer
from django.conf import settings

def get_video_player():

	video_players = VideoPlayer.objects.all()
	for video_player in video_players:
		player = str(video_player)
		if os.path.exists(player):
			return player

	raise Exception('No video player found.')

def play_video(video_path):

	try:
		video_path = os.path.join(settings.VIDEO_PATH, video_path)

		return subprocess.call([ get_video_player(), video_path ]), 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

def stop_video(video_path):

	try:
		return subprocess.call([ 'killall', get_video_player() ]), 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

def open_door(pin):

	try:
		ret = 0
		#ret = GPIO.output(pin, True)
		return ret, 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

def close_door(pin):

	try:
		ret = 0
		#ret = GPIO.output(pin, False)
		return ret, 'Success'

	except Exception as err:
		return 1, "Error: %s" % err

