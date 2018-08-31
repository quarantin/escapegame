#!/bin/bash

SCRIPTDIR="$(dirname "${0}")"

ROOTDIR="$(realpath "${SCRIPTDIR}/..")"

. "${ROOTDIR}/master-hostname.txt"

MASTER_HOSTNAME_SHORT="${HOSTNAME}"
MASTER_HOSTNAME="${HOSTNAME}${TLD}"

HOSTNAME="$(hostname)${TLD}"

PIP=pip3

PYTHON=python3

PYTHON_BIN=/usr/bin/python3.5

MYSQL_ARCHIVE=/tmp/mysql-lib-folder.tar.gz

PLAYER_FIFO=/tmp/video-control.fifo

RUNNING_ON_PI=true
if [ "$(lsb_release -a -s 2>/dev/null | grep Raspbian | wc -l)" -eq "0" ]; then
	RUNNING_ON_PI=false
fi
