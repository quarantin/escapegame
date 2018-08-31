#!/bin/bash -x

. $(dirname $0)/env.sh

TIMEZONE='Europe/Paris'

ARCH=amd64
NGINX_PKG=nginx-full
if [ "$RUNNING_ON_PI" = true ]; then
	ARCH=armv6l
	NGINX_PKG=nginx-light
fi

DEBIAN_PACKAGES=(
	bc
	mysql-server
	$NGINX_PKG
	redis-server
	screen
	uwsgi
	uwsgi-plugin-python3
	vim
)

PIP_PACKAGES=(
	channels
	django
	django-background-tasks
	django-constance[database]
	django-cors-headers
	django-extensions
	django-redis-sessions
	django-rest-framework
	django-websocket-redis==0.5.2
	mysqlclient
	omxplayer-wrapper
	service_identity
)

DJANGO='django'
WEBSOCKET='websocket'

SOCKET_DJANGO="/tmp/uwsgi.${DJANGO}.socket"
SOCKET_WEBSOCKET="/tmp/uwsgi.${WEBSOCKET}.socket"

NGINX_CONF='nginx.conf'
NGINX_SITES_ENABLED='/etc/nginx/sites-enabled'
NGINX_SITES_AVAILABLE='/etc/nginx/sites-available'

UWSGI_CONF='uwsgi.ini'
UWSGI_CONF_DEFAULT='defaults.ini'
UWSGI_APPS_ENABLED='/etc/uwsgi/apps-enabled'
UWSGI_APPS_AVAILABLE='/etc/uwsgi/apps-available'

REDIS_CONFIG='/etc/redis/redis.conf'
MYSQL_CONFIG='/etc/mysql/mysql.conf.d/mysqld.cnf'

# Install Debian packages
sudo apt-get install --yes --quiet "${DEBIAN_PACKAGES[@]}"

# Install pip packages
sudo -H ${PIP} install --quiet "${PIP_PACKAGES[@]}"

# Install golang 1.11
GOLANG_VERSION=1.11
GOLANG_PKG="go${GOLANG_VERSION}.linux-${ARCH}.tar.gz"
GOLANG_URL="https://storage.googleapis.com/golang/${GOLANG_PKG}"
wget -q -O "/tmp/${GOLANG_PKG}" "${GOLANG_URL}"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xf "/tmp/${GOLANG_PKG}"
rm -f "/tmp/${GOLANG_PKG}"

# Install arduino-cli
GO_DIR=~/golang
rm -rf ${GO_DIR}
mkdir -p ${GO_DIR}
export GOPATH=${GO_DIR}
go get -u github.com/arduino/arduino-cli
mkdir -p ~/.arduino15
${GO_DIR}/bin/arduino-cli core update-index
${GO_DIR}/bin/arduino-cli core install arduino:avr

# Install github.com/elechouse/PN532 (NFC library for Arduino)
PN532_PKG=PN532_HSU.zip
PN532_URL="https://github.com/elechouse/PN532/archive/${PN532_PKG}"
ARDUINO_LIBS=~/Arduino/libraries/
mkdir -p ${ARDUINO_LIBS}
rm -rf ${ARDUINO_LIBS}/*
wget -q -O "/tmp/${PN532_PKG}" "${PN532_URL}"
unzip -q "/tmp/${PN532_PKG}" -d ${ARDUINO_LIBS}
rm -f "/tmp/${PN532_PKG}"
mv ${ARDUINO_LIBS}/PN532-PN532_HSU/* ${ARDUINO_LIBS}
rmdir "${ARDUINO_LIBS}/PN532-PN532_HSU"

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

# Disable server tokens for nginx (hide the version)
sudo sed -i 's/# server_tokens off/server_tokens off/' /etc/nginx/nginx.conf

# Remove default and old configs of nginx and uwsgi
sudo rm -f                     \
	${NGINX_SITES_ENABLED}/*   \
	${NGINX_SITES_AVAILABLE}/* \
	${UWSGI_APPS_ENABLED}/*    \
	${UWSGI_APPS_AVAILABLE}/*

# Deploy our custom nginx and uwsgi configs
sudo cp "${ROOTDIR}/conf/${NGINX_CONF}" "${NGINX_SITES_AVAILABLE}/${NGINX_CONF}"
sudo cp "${ROOTDIR}/conf/${UWSGI_CONF}" "${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF}"
sudo cp "${ROOTDIR}/conf/${UWSGI_CONF_DEFAULT}" "${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF_DEFAULT}"

CONFIGS=(
	"${NGINX_SITES_AVAILABLE}/${NGINX_CONF}"
	"${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF}"
	"${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF_DEFAULT}"
)

# Substitue our placeholder variables
for CONFIG in "${CONFIGS[@]}"; do

	sudo sed -i                                        \
		-e "s#<ROOTDIR>#${ROOTDIR}#"                   \
		-e "s#<HOSTNAME>#${HOSTNAME}#"                 \
		-e "s#<SOCKET_DJANGO>#${SOCKET_DJANGO}#"       \
		-e "s#<SOCKET_WEBSOCKET>#${SOCKET_WEBSOCKET}#" \
		$CONFIG
done

# Configure mysql to listen on the network
sudo sed -i 's/^bind-address        = 127.0.0.1$/bind = 0.0.0.0/' "${MYSQL_CONFIG}" || true

# Configure redis to listen on the network
sudo sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/' "${REDIS_CONFIG}" || true

# Creates corresponding symlinks
sudo ln -s -r -t "${NGINX_SITES_ENABLED}/" "${NGINX_SITES_AVAILABLE}/${NGINX_CONF}"
sudo ln -s -r -t "${UWSGI_APPS_ENABLED}/"  "${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF}"
sudo ln -s -r -t "${UWSGI_APPS_ENABLED}/"  "${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF_DEFAULT}"

# Enable nginx service at boot time
sudo update-rc.d nginx defaults

# Enable uwsgi services at boot time
"${ROOTDIR}/scripts/set-crontab.sh"

# Restart all services
"${ROOTDIR}/scripts/restart-all.sh"
