#!/bin/bash

. $(dirname $0)/env.sh

cd /var/lib/

echo 'Copying mysql archive from master host'
scp pi@${MASTER_HOSTNAME}:"${MYSQL_ARCHIVE}" /tmp
if [ "$?" -ne "0" ]; then
	echo "Failed to download archive ${MYSQL_ARCHIVE} from host ${MASTER_HOSTNAME}"
	exit
fi

# Stopping MySQL
sudo /etc/init.d/mysql stop

# Extract tar archive into /var/lib/mysql folder
echo 'Extracting mysql archive into /var/lib/mysql'
sudo tar xf "${MYSQL_ARCHIVE}"

# Starting MySQL
sudo /etc/init.d/mysql start
