#!/bin/bash

. $(dirname $0)/env.sh

DEBIAN_PACKAGES=( 'sqlite3' 'vim' 'screen' )

PIP_PACKAGES=( 'django' 'django-cors-headers' 'django-background-tasks' 'django-constance[database]' )

sudo apt-get install "${DEBIAN_PACKAGES[@]}"

sudo -H ${PIP} install "${PIP_PACKAGES[@]}"

if [ "$USER" = "pi" ]; then
cat << EOF > ~/.vimrc
syntax on
set ic
set hlsearch
set tabstop=4 noexpandtab
EOF
fi
