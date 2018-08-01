# -*- coding: utf-8 -*-

from django_admin_conf_vars.global_vars import config

import os

running_on_pi = True
default_player = 'omxplayer'

if not ' '.join(os.uname()).strip().endswith('armv7l'):
	running_on_pi = False
	default_player = 'mpv'

config.set('RUNNING_ON_PI', default=running_on_pi)
config.set('VIDEO_PATH', default='/opt/vc/src/hello_pi/hello_video')
config.set('VIDEO_PLAYER', default=default_player)
