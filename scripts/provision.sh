#!/bin/bash

. $(dirname $0)/env.sh

DEBIAN_PACKAGES=( 'sqlite3' 'vim' 'screen' )

PIP_PACKAGES=( 'django' 'django-cors-headers' 'django-background-tasks' 'django-constance[database]' )

sudo apt-get install "${DEBIAN_PACKAGES[@]}"

sudo -H ${PIP} install "${PIP_PACKAGES[@]}"

if [ "$USER" = "pi" ]; then
echo <<< EOF
syntax on
set tabstop=8 noexpandtab
EOF >> ~/.vimrc
fi
