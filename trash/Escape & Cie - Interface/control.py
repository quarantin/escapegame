from bottle import route, run, template, request, static_file
import RPi.GPIO as GPIO
from threading import Thread, Event, Timer
import time 
import subprocess
import sys

IP_ADDRESS= 'raspberrypi.local'

GPIO.setmode(GPIO.BCM)

DOOR_1001_NUITS = 1

DOOR_STRANGER_THINGS = 2
GPIO.setup(DOOR_1001_NUITS, GPIO.OUT)
GPIO.setup(DOOR_STRANGER_THINGS, GPIO.OUT)

# class VideoPlayer(Thread):
#     "Launch the video, after killing the others"
#     def __init__(self, video_path):

#         Thread.__init__(self)
#         # self.logfile= open('/tmp/mylogfile', 'w+')
#         self.video_path = video_path
#         self.do_launch = Event()
#         self.daemon = True
#         self.start()

#     def run(self):
#         while True:
#             self.do_launch.wait()
#             self.do_launch.clear()
#             subprocess.call(["killall", "omxplayer.bin"])
#             logging.debug("Killed all omxplayer")
#             play_process = subprocess.Popen(['omxplayer', self.video_path],
#                 stdin=subprocess.PIPE,
#                 stdout=sys.stdout, 
#                 # subprocess.PIPE,
#                 stderr=sys.stderr,
#                 # subprocess.PIPE,

#                 close_fds=True)
#             logging.debug("Video started")

#     def launch(self):
#         self.do_launch.set()


def open_door(pin, duration):
	GPIO.output(pin, True)
	time.sleep(duration)
	GPIO.output(pin, False)

def close_door(pin):
	GPIO.output(pin, False)

def play_video():
    video_path = '/opt/vc/src/hello_pi/hello_video/test.h264'
    ret = subprocess.call(['omxplayer', video_path])


#def change_led_color():
	
@route('/')
def index(name='time'):
	return template('index.tpl')

@route('/img/:path#.+#')
def server_static(path):
	return static_file(path, root='img/')

@route('/css/:path#.+#')
def server_static(path):
	return static_file(path, root='css/')

@route('/bootstrap/:path#.+#')
def server_static(path):
	return static_file(path, root='bootstrap/')

@route('/1001_nuits')
def control_1001_nuits():
   return template('1001_nuits.tpl')

@route('/1001_nuits', method='POST')
def do_control_1001_nuits():
	action = request.forms.get('executer')

	if action == 'brief_nuits':
		# play_video_nuit= VideoPlayer('/opt/vc/src/hello_pi/hello_video/test.h264')
		play_video()

	if action =='Open_jardin':
		open_door(1, 10)

	if action == 'Open_caverne':
		open_door(1, 10)

	if action == 'Open_lampe':
		open_door(1, 10)
	
	# return template('1001_nuits.tpl')




@route('/stranger-things')
def control_stranger_things(name='', method= 'POST'):
	return template('stranger-things.tpl')
	action = request.POST.get('executer')


	if action == 'brief_stranger':
		# play_video_stranger=VideoPlayer('/opt/vc/src/hello_pi/hello_video/test.h264')
		play_video()
		
	if action == 'Open_sombre':
		open_door(1, 10)

	if action == 'Open_clair':
		open_door(1, 10)

	if action == 'Open_wood':
		open_door(1, 10)

	if action == 'Open_cabane':
		open_door(1, 10)

try:
	run(host=IP_ADDRESS, port=80)
finally: 
	print('Cleaning up GPIO')
	GPIO.cleanup()