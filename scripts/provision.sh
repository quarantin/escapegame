#!/bin/bash -e

. $(dirname $0)/env.sh

TIMEZONE='Europe/Paris'

ARCH=amd64
NGINX_PKG=nginx-full
MYSQL_CONFIG='/etc/mysql/mysql.conf.d/mysqld.cnf'
if [ "$RUNNING_ON_PI" = true ]; then
	ARCH=armv6l
	NGINX_PKG=nginx-light
	if [ "$RUNNING_ON_PI_V3" = true ]; then
		MYSQL_CONFIG='/etc/mysql/mariadb.conf.d/50-server.cnf'
	fi

fi

DEBIAN_PACKAGES=(
	bc
	git
	libdbd-mysql-perl
	munin-node
	$NGINX_PKG
	python3
	python3-pip
	screen
	uwsgi
	uwsgi-plugin-python3
	vim
)

SERVER_PACKAGES=(
	munin
	mysql-server
	redis-server
)

# Only the master needs mysql and redis
if [ $HOSTNAME == $MASTER_HOSTNAME ]; then
	DEBIAN_PACKAGES+=( "${SERVER_PACKAGES[@]}" )
fi

PIP_PACKAGES=(
	asn1crypto==0.24.0
	cffi==1.11.5
	channels==2.1.3
	cryptography==2.3.1
	django==2.0.7
	django-constance[database]==2.2.0
	django-cors-headers==2.4.0
	django-extensions==2.1.0
	django-redis-sessions==0.6.1
	django-rest-framework==0.1.0
	django-websocket-redis==0.5.2
	gevent==1.3.6
	greenlet==0.4.14
	mysqlclient==1.3.13
	pyasn1==0.4.4
	pyOpenSSL==18.0.0
	redis==2.10.6
	service_identity==17.0.0
	six==1.10.0
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

# TODO select en_US.UTF-8 and fr_FR.UTF-8
# TODO sudo dpkg-reconfigure locales

# Install Debian packages
echo "Installing the following Debian packages: ${DEBIAN_PACKAGES[@]}"
sudo apt-get install --yes --quiet "${DEBIAN_PACKAGES[@]}"

# Install pip packages
echo "Installing the following pip packages: ${PIP_PACKAGES[@]}"
sudo -H ${PIP} install "${PIP_PACKAGES[@]}"

# Install golang 1.11
GOLANG_VERSION=1.11
GOLANG_PKG="go${GOLANG_VERSION}.linux-${ARCH}.tar.gz"
GOLANG_URL="https://storage.googleapis.com/golang/${GOLANG_PKG}"
wget -q -O "/tmp/${GOLANG_PKG}" "${GOLANG_URL}"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xf "/tmp/${GOLANG_PKG}"
export GOROOT=/usr/local/go
export PATH=$PATH:$GOROOT/bin
rm -f "/tmp/${GOLANG_PKG}"

# Install arduino-cli
GO_DIR=~/golang
rm -rf ${GO_DIR}
mkdir -p ${GO_DIR}
export GOPATH=${GO_DIR}
export PATH=$PATH:$GOPATH
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
sudo timedatectl set-timezone ${TIMEZONE}

# Hide GNU screen startup message
sudo sed -i 's/^#startup_message off$/startup_message off/' /etc/screenrc

# Disable server tokens for nginx (hide the version)
sudo sed -i 's/# server_tokens off/server_tokens off/' /etc/nginx/nginx.conf

# Configure munin-node
sudo munin-node-configure --shell --families=contrib,auto | sudo sh -x

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

if [ $HOSTNAME == $MASTER_HOSTNAME ]; then

	# Configure mysql to listen on the network
	sudo sed -i 's/^bind-address[^a-z]*= 127.0.0.1$/bind-address = 0.0.0.0/' "${MYSQL_CONFIG}" || true

	# Configure redis to listen on the network
	REDIS_CONFIG='/etc/redis/redis.conf'
	sudo sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/' "${REDIS_CONFIG}" || true
fi

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
