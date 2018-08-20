#!/bin/bash

. $(dirname $0)/env.sh

TIMEZONE='Europe/Paris'
DEBIAN_PACKAGES=( 'bc' 'screen' 'sqlite3' 'mysql-server' 'nginx-full' 'redis-server' 'uwsgi' 'uwsgi-plugin-python3' 'vim' )

PIP_PACKAGES=( 'channels' 'django' 'django-background-tasks' 'django-constance[database]' 'django-cors-headers' 'django-extensions' 'django-rest-framework' 'django-websocket-redis' 'mysqlclient' )

NGINX_CONF=django.conf
DJANGO_CONF=django.ini
WEBSOCKET_CONF=websocket.ini

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
sudo timedatectl set-timezone "${TIMEZONE}"

# Hide GNU screen startup message
sudo sed -i 's/^#startup_message off$/startup_message off/' /etc/screenrc

# Remote default and old configs of nginx and uwsgi
sudo rm -f /etc/uwsgi/apps-enabled/*
sudo rm -f /etc/nginx/sites-enabled/*

# Deploy our custom nginx and uwsgi configs
sudo cp "${ROOTDIR}/conf/escapegame.uwsgi.django.ini" /etc/uwsgi/apps-available/${DJANGO_CONF}
sudo cp "${ROOTDIR}/conf/escapegame.uwsgi.websocket.ini" /etc/uwsgi/apps-available/${WEBSOCKET_CONF}
sudo cp "${ROOTDIR}/conf/escapegame.nginx.conf" /etc/nginx/sites-available/${NGINX_CONF}

# Replace <ROOTDIR> placeholder with correct root folder (django root)
sudo sed -i "s#<ROOTDIR>#${ROOTDIR}#" /etc/uwsgi/apps-available/*
sudo sed -i "s#<ROOTDIR>#${ROOTDIR}#" /etc/nginx/sites-available/${NGINX_CONF}
sudo sed -i "s#<HOSTNAME>#$(hostname).local#" /etc/nginx/sites-available/${NGINX_CONF}

# Disable server tokens for nginx (hide the version)
sudo sed -i 's/# server_tokens off/server_tokens off/' /etc/nginx/nginx.conf

# Creates corresponding symlinks
sudo ln -s -r -t /etc/uwsgi/apps-enabled/ /etc/uwsgi/apps-available/${DJANGO_CONF}
sudo ln -s -r -t /etc/uwsgi/apps-enabled/ /etc/uwsgi/apps-available/${WEBSOCKET_CONF}
sudo ln -s -r -t /etc/nginx/sites-enabled/ /etc/nginx/sites-available/${NGINX_CONF}

# Enable uwsgi and nginx init scripts at boot time
sudo update-rc.d uwsgi defaults
sudo update-rc.d nginx defaults

# Restart uwsgi and nginx services
sudo /etc/init.d/uwsgi restart
sudo /etc/init.d/nginx restart
