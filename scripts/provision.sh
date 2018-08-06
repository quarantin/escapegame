#!/bin/bash

. $(dirname $0)/env.sh

DEBIAN_PACKAGES=( 'sqlite3' 'vim' 'screen' 'mysql-server' )

PIP_PACKAGES=( 'django' 'django-cors-headers' 'django-background-tasks' 'django-constance[database]' 'mysqlclient' )

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

sudo sed -i 's/^#startup_message off$/startup_message off/' /etc/screenrc
