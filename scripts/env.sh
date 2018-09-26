#!/bin/bash -e

SCRIPTDIR="$(dirname "${0}")"

ROOTDIR="$(realpath "${SCRIPTDIR}/..")"

. "${ROOTDIR}/master-hostname.txt"

MASTER_HOSTNAME="${HOSTNAME}${TLD}"

HOSTNAME="$(hostname)${TLD}"

PI_UID=1000
PI_GID=1000

PIP=pip3

PYTHON=python3

PYTHON_BIN=/usr/bin/python3.5

MYSQL_ARCHIVE=/tmp/mysql-lib-folder.tar.gz

PLAYER_FIFO=/tmp/video-control.fifo

CPU=$(uname -a | awk '{ print $(NF-1) }')

[[ ${CPU} == 'armv'* ]] && RUNNING_ON_PI=true || RUNNING_ON_PI=false
