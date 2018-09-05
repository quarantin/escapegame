# -*- coding: utf-8 -*-

from constance import config

import os
import dbus
import getpass
import traceback
import subprocess


#
# Generic video player
#
class BaseVideoPlayer():

	def __init__(self, socket, video_url):

		self.socket = socket
		self.video_url = video_url

	def get_available_actions(self):
		return [
			'pause',
			'play',
			'stop',
		]

	def pause(self):
		pass

	def play(self):
		pass

	def stop(self):
		pass

	def control(self, action):

		try:
			actions = self.get_available_actions()
			if action not in actions:
				raise Exception('Invalid action `%s`' % action)

			return getattr(self, action)()

		except Exception as err:
			return 1, 'Error: %s' % traceback.format_exc()

#
# Player class: mpv
#
class PlayerMPV(BaseVideoPlayer):

	def __init__(self, video_url, socket='/tmp/mpv.fifo'):
		super(PlayerMPV, self).__init__(socket, video_url)

	def pause(self):

		try:
			status, message = 1, 'Fifo %s could not be found' % self.socket
			if os.path.exists(self.socket):
				fout = open(self.socket, 'w')
				fout.write('pause\n')
				fout.close()
				status, message = 0, 'Success'

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % traceback.format_exc()

	def play(self, video_url=None):

		try:

			socket_exists = os.path.exists(self.socket)
			# TODO toggle play/pause
			#if socket_exists and video_url is None or video_url == self.video_url:
			#	return self.pause()

			if video_url is not None:
				self.video_url = video_url
			else:
				video_url = self.video_url

			status, message = 1, 'Fifo %s could not be found' % self.socket
			if socket_exists:
				os.remove(self.socket)

			os.mkfifo(self.socket)

			#p = subprocess.Popen([ config.VIDEO_PLAYER, '--input-file', self.socket, video_url ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
			p = subprocess.Popen([ config.VIDEO_PLAYER, '--input-file', self.socket, video_url ], close_fds=True)
			#p.wait()
			#print('Flusing stderr from player:')
			#print(p.stderr.read())

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % traceback.format_exc()

	def stop(self):

		try:
			#os.system('killall mpv; rm -f %s' % fifo)
			#return 0, 'Success'

			status, message = 1, 'Fifo %s could not be found' % self.socket
			if os.path.exists(self.socket):
				fout = open(self.socket, 'w')
				fout.write('stop\n')
				fout.close()
				status, message = 0, 'Success'

			return status, message

		except Exception as err:
			return 1, 'Error: %s' % traceback.format_exc()

#
# Player: omxplayer
#
class PlayerOMX(BaseVideoPlayer):

	if config.RUNNING_ON_PI:
		from omxplayer import keys, player
		from omxplayer.bus_finder import BusFinder

	controls = None
	properties = None

	def __init__(self, video_url, socket='org.mpris.MediaPlayer2.omxplayer'):
		super(PlayerOMX, self).__init__(socket, video_url)

		# Starts the video
		self.play(video_url)

		# Initialize DBUS controls and properties
		self.__init_controls()

	def __init_controls(self):

		try:
			socket_path = '/tmp/omxplayerdbus.%s' % getpass.getuser()
			if not os.path.exists(socket_path):
				socket_path = '/tmp/omxplayerdbus.root'
				if not os.path.exists(socket_path):
					return

			# Get the bus connection of omxplayer
			bus = dbus.bus.BusConnection(BusFinder().get_address())

			# Retrieve omxplayer dbus handle
			handle = bus.get_object(self.socket, '/org/mpris/MediaPlayer2', introspect=False)

			# Retrieve omxplayer controls and properties through dbus handle
			self.controls = dbus.Interface(handle, 'org.mpris.MediaPlayer2.Player')
			self.properties = dbus.Interface(handle, 'org.freedesktop.DBus.Properties')

		except Exception as err:
			pass

	def __basic_control(self, key):

		try:
			if not self.controls:

				self.__init_controls()
				if not self.controls:
					return 1, 'No video running'

			self.controls.Action(key)
			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % err

	def __basic_property(self, key):

		try:
			if not self.properties:

				self.__init_controls()
				if not self.properties:
					return

			return self.properties.Get(key)

		except Exception as err:
			return 1, 'Error: %s' % err

	def duration(self):
		return self.__basic_property('Duration')

	def fast_forward(self):
		return self.__basic_control(keys.FAST_FORWARD)

	def pause(self):
		return self.__basic_control(keys.PAUSE)

	def play(self, video_url=None):

		if video_url is None:
			return self.pause()

		self.video_url = video_url
		player.OMXPlayer(video_url, pause=False, dbus_name=self.socket, args=[ '--no-osd' ])

	def position(self):
		return self.__basic_property('Position')

	def stop(self):
		return self.__basic_control(keys.EXIT)

	def rewind(self):
		return self.__basic_control(keys.REWIND)

if config.RUNNING_ON_PI:

	class VideoPlayer(PlayerOMX):
		pass
else:

	class VideoPlayer(PlayerMPV):
		pass
