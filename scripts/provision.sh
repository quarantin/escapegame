#!/bin/bash

. $(dirname $0)/env.sh

DEBIAN_PACKAGES=( sqlite3 )

PIP_PACKAGES=( django django-admin-conf-vars )

sudo apt-get install "${DEBIAN_PACKAGES[@]}"

sudo -H ${PIP} install "${PIP_PACKAGES[@]}"
