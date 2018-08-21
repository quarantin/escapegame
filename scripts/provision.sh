#!/bin/bash -x

. $(dirname $0)/env.sh

TIMEZONE='Europe/Paris'
DEBIAN_PACKAGES=( 'bc' 'screen' 'sqlite3' 'mysql-server' 'nginx-full' 'redis-server' 'uwsgi' 'uwsgi-plugin-python3' 'vim' )

PIP_PACKAGES=( 'channels' 'django' 'django-background-tasks' 'django-constance[database]' 'django-cors-headers' 'django-extensions' 'django-redis-sessions' 'django-rest-framework' 'django-websocket-redis' 'mysqlclient' )

DJANGO='django'
WEBSOCKET='websocket'

SOCKET_DJANGO="/tmp/uwsgi.${DJANGO}.socket"
SOCKET_WEBSOCKET="/tmp/uwsgi.${WEBSOCKET}.socket"

NGINX_CONF='nginx.conf'
NGINX_SITES_ENABLED='/etc/nginx/sites-enabled'
NGINX_SITES_AVAILABLE='/etc/nginx/sites-available'

UWSGI_CONF='uwsgi.ini'
UWSGI_APPS_ENABLED='/etc/uwsgi/apps-enabled'
UWSGI_APPS_AVAILABLE='/etc/uwsgi/apps-available'

# Install Debian packages
sudo apt-get install --yes --quiet "${DEBIAN_PACKAGES[@]}"

# Install pip packages
sudo -H ${PIP} install --quiet "${PIP_PACKAGES[@]}"

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
sudo cp "${ROOTDIR}/conf/${UWSGI_CONF}" "${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF}"
sudo cp "${ROOTDIR}/conf/${NGINX_CONF}" "${NGINX_SITES_AVAILABLE}/${NGINX_CONF}"

CONFIGS=(
	"${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF}"
	"${NGINX_SITES_AVAILABLE}/${NGINX_CONF}"
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


# Creates corresponding symlinks
sudo ln -s -r -t "${UWSGI_APPS_ENABLED}/"  "${UWSGI_APPS_AVAILABLE}/${UWSGI_CONF}"
sudo ln -s -r -t "${NGINX_SITES_ENABLED}/" "${NGINX_SITES_AVAILABLE}/${NGINX_CONF}"

# Enable nginx service at boot time
sudo update-rc.d nginx defaults

# Restart nginx service
sudo /etc/init.d/nginx restart

# Enable uwsgi services at boot time
"${ROOTDIR}/scripts/set-crontab.sh"

# Restart uwsgi services
"${ROOTDIR}/scripts/restart-uwsgi.sh"
