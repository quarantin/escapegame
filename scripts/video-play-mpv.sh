#!/bin/bash

. $(dirname $0)/env.sh

mkfifo $PLAYER_FIFO 2> /dev/null

mpv --input-file $PLAYER_FIFO /opt/vc/src/hello_pi/hello_video/test.h264
