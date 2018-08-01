# -*- coding: utf-8 -*-

from django_admin_conf_vars.global_vars import config

import os

default_player = 'omxplayer'
if not ' '.join(os.uname()).strip().endswith('armv7l'):
	default_player = 'mpv'

config.set('VIDEO_PATH', default='/opt/vc/src/hello_pi/hello_video')
config.set('VIDEO_PLAYER', default=default_player)
