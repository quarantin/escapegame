#!/bin/bash

PIP=pip3

PYTHON=python3

PYTHON_BIN=/usr/bin/python3.5

SCRIPTDIR="$(dirname "${0}")"

ROOTDIR="$(realpath "${SCRIPTDIR}/..")"

HOSTNAME="$(hostname).local"

MYSQL_ARCHIVE=/tmp/mysql-lib-folder.tar.gz

PLAYER_FIFO=/tmp/video-control.fifo
