from django.conf import settings
import subprocess, time
#import RPi.GPIO as GPIO

default_video_path ='/opt/vc/src/hello_pi/hello_video/test.h264'

def open_door(pin, duration):
	#GPIO.output(pin, True)
	time.sleep(duration)
	#GPIO.output(pin, False)

def close_door(pin):
	#GPIO.output(pin, False)
	time.sleep(1)

def play_video(video_path=default_video_path):
	subprocess.call([ 'killall', settings.VIDEO_PLAYER ])
	subprocess.call([ settings.VIDEO_PLAYER, video_path ])
