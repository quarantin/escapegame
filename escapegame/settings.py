# -*- coding: utf-8 -*-

from django_admin_conf_vars.global_vars import config

import os

default_media_root = '/home/pi/media'
default_media_url = '/media/'
default_upload_path = 'uploads'
default_video_path = '/opt/vc/src/hello_pi/hello_video'
default_video_player = 'omxplayer'
running_on_pi = True

if not ' '.join(os.uname()).strip().endswith('armv7l'):
	default_media_root = '/tmp'
	default_video_player = 'mpv'
	running_on_pi = False

config.set('MEDIA_ROOT', default=default_media_root)
config.set('MEDIA_URL', default=default_media_url)
config.set('RUNNING_ON_PI', default=running_on_pi)
config.set('UPLOAD_PATH', default=default_upload_path)
config.set('VIDEO_PATH', default=default_video_path)
config.set('VIDEO_PLAYER', default=default_video_player)
