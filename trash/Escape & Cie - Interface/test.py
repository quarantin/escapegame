#!/usr/bin/python3

class VideoPlayer(Thread):
    "Launch the video, after killing the others"
    def __init__(self, video_path):

        Thread.__init__(self)
        # self.logfile= open('/tmp/mylogfile', 'w+')
        self.video_path = video_path
        self.do_launch = Event()
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self.do_launch.wait()
            self.do_launch.clear()
            subprocess.call(["killall", "omxplayer.bin"])
            logging.debug("Killed all omxplayer")
            play_process = subprocess.Popen(['omxplayer', self.video_path],
                stdin=subprocess.PIPE,
                stdout=sys.stdout, 
                # subprocess.PIPE,
                stderr=sys.stderr,
                # subprocess.PIPE,

                close_fds=True)
            logging.debug("Video started")

    def launch(self):
        self.do_launch.set()

video_path = '/opt/vc/src/hello_pi/hello_video/test.h264'
test = VideoPlayer(video_path)