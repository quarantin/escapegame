#!/bin/bash

. $(dirname $0)/env.sh

mkfifo $PLAYER_FIFO 2> /dev/null

cat $PLAYER_FIFO | omxplayer /opt/vc/src/hello_pi/hello_video/test.h264
