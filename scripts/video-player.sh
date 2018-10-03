#!/bin/bash

. $(dirname $0)/env.sh

if [ -z ${1} ] || [ -z ${2} ] || [ -z ${3} ]; then
	echo "Usage: $0 <fifo> <audio-out> <url>"
	exit
fi

FIFO=${1}
if [ ! -p ${FIFO} ]; then
	mkfifo ${FIFO}
fi

AUDIO_OUT=${2}

URL=${3}

if [ ${RUNNING_ON_PI} = true ]; then

	# omxplayer needs to receive a newline on
	# the FIFO to start playing the video.
	echo > ${FIFO} &

	/usr/bin/omxplayer --no-osd --adev ${AUDIO_OUT} ${URL} < ${FIFO}
else
	/usr/bin/mpv --input-file ${FIFO} ${URL}
fi

rm -f ${FIFO}
