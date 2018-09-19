#!/bin/bash

SCRIPTDIR="$(dirname "${0}")"

ROOTDIR="$(realpath "${SCRIPTDIR}/..")"

. "${ROOTDIR}/master-hostname.txt"

MASTER_HOSTNAME="${HOSTNAME}${TLD}"

HOSTNAME="$(hostname)${TLD}"

PIP=pip3

PYTHON=python3

PYTHON_BIN=/usr/bin/python3.5

MYSQL_ARCHIVE=/tmp/mysql-lib-folder.tar.gz

PLAYER_FIFO=/tmp/video-control.fifo

CPU=$(uname -a | awk '{ print $(NF-1) }')

RUNNING_ON_PI=true
RUNNING_ON_PI_V3=true

if [[ ${CPU} == 'armv*' ]]; then

	if [ ${CPU} != 'armv7l' ]; then
		RUNNING_ON_PI_V3=$?
	fi

else
	RUNNING_ON_PI=false
	RUNNING_ON_PI_V3=false
fi
