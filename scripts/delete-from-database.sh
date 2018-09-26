#!/bin/bash

. $(dirname $0)/env.sh

cd ${ROOTDIR}

mysql -e 'SET FOREIGN_KEY_CHECKS=0'

for table in $(${PYTHON} manage.py show-tables); do
	echo "Deleting from table \`${table}\`"
	mysql -e "SET FOREIGN_KEY_CHECKS=0; DELETE FROM ${table}"
done

mysql -e 'SET FOREIGN_KEY_CHECKS=1'
