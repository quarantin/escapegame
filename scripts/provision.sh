#!/bin/bash

. $(dirname $0)/env.sh

DEBIAN_PACKAGES=( 'sqlite3' 'vim' 'screen' 'mysql-server' )

PIP_PACKAGES=( 'django' 'django-cors-headers' 'django-background-tasks' 'django-constance[database]' 'mysqlclient' )

# Install Debian packages
sudo apt-get install "${DEBIAN_PACKAGES[@]}"

# Install pip packages
sudo -H ${PIP} install "${PIP_PACKAGES[@]}"

# Creates default ~/.vimrc
if [ "$USER" = "pi" ]; then
cat << EOF > ~/.vimrc
syntax on
set ic
set hlsearch
set tabstop=4 noexpandtab
EOF
fi

# Configure timezone
sudo timedatectl set-timezone Europe/Paris

# Hide GNU screen startup message
sudo sed -i 's/^#startup_message off$/startup_message off/' /etc/screenrc
