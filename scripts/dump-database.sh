#!/bin/bash

. $(dirname $0)/env.sh

cd /var/lib/

# Stopping MySQL
sudo /etc/init.d/mysql stop

# Creating tar archive of /var/lib/mysql folder
echo 'Dumping mysql /var/lib folder into archive...'
sudo tar czf $MYSQL_ARCHIVE mysql/

# Starting MySQL
sudo /etc/init.d/mysql start
