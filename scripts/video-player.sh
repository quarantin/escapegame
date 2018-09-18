#!/bin/bash

. $(dirname $0)/env.sh

if [ -z ${1} ] || [ -z ${2} ]; then
	echo "Usage: $0 <fifo> <url>"
	exit
fi

FIFO=${1}
if [ ! -p ${FIFO} ]; then
	mkfifo ${FIFO}
fi

URL=${2}
if [ ${RUNNING_ON_PI} = true ]; then

	# omxplayer needs to receive a newline on
	# the FIFO to start playing the video.
	echo > ${FIFO} &

	/usr/bin/omxplayer --no-osd ${URL} < ${FIFO}
else
	/usr/bin/mpv --input-file ${FIFO} ${URL}
fi

rm -f ${FIFO}
