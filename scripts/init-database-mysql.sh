#!/bin/bash -e

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

DBNAME=escapegame
DBUSER=escapegame
DBPASS=escapegame
DBPORT=3306

# Ask sudo password before anything else to avoid polluting script output.
sudo echo > /dev/null

CREATE_MYSQL_CLIENT_CONFIG(){

	DBHOST=$1

	echo -n "[ * ] Creating MySQL client configuration for \`${DBHOST}\`... "

	# Create MySQL user config
	cat <<EOF > ${HOME}/.my.cnf
[client]
host = ${DBHOST}
port = ${DBPORT}
database = ${DBNAME}
user = ${DBUSER}
password = ${DBPASS}
default-character-set = utf8
EOF
	echo OK
}

CREATE_MYSQL_ROOT_CONFIG(){

	echo -n '[ * ] Reseting MySQL client configuration... '

	# Reset mysql client configuration
	echo "[client]" > "${HOME}/.my.cnf"

	DBHOST=localhost

	echo OK
}

KILL_MYSQL_TASKS(){

	echo -n '[ * ] Killing MySQL tasks... '

	KILL_COMMAND=$(sudo mysql -u root -e "show processlist" | tail -n +2 | grep -v 'show processlist'  | awk -F"\t" '{ print $1}' | sed -e 's/^/KILL /' -e 's/$/;/' | tr '\n' ' ')
	if [ -z "${KILL_COMMAND}" ]; then
		echo 'OK (No task found)'
	else
		sudo mysql -u root -e "${KILL_COMMAND}"
		echo OK
	fi
}

CREATE_MYSQL_DATABASE(){

	echo -n "[ * ] Creating MySQL database \`${DBNAME}\`... "

	sudo mysql -u root -e "DROP DATABASE IF EXISTS ${DBNAME}"
	sudo mysql -u root -e "CREATE DATABASE ${DBNAME} CHARACTER SET utf8"

	echo OK
}

CREATE_MYSQL_USER(){

	DB_HOST=$1

	MYSQL_VERSION=$(sudo mysql -s -N -e "select @@version")
	VERSION_PREFIX=$(echo $MYSQL_VERSION | tr '.' '\n' | head -n 2 | tr '\n' '.' | sed 's/\.$//')
	SUPPORT_IF_EXISTS=$(echo "$VERSION_PREFIX>=5.7" | bc)
	IF_EXISTS=''
	if [ "$SUPPORT_IF_EXISTS" -eq '1' ]; then
		IF_EXISTS='IF EXISTS '
	fi

	echo -n "[ * ] Creating MySQL user for \`${DBUSER}\`@\`${DB_HOST}\` on database \`${DBNAME}\`... "

	sudo mysql -u root -e "DROP USER ${IF_EXISTS} '${DBUSER}'@'${DB_HOST}'"
	sudo mysql -u root -e "CREATE USER '${DBUSER}'@'${DB_HOST}' IDENTIFIED BY '${DBPASS}'"
	sudo mysql -u root -e "GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '${DBUSER}'@'${DB_HOST}'"
	sudo mysql -u root -e "GRANT ALL PRIVILEGES ON test_${DBNAME}.* TO '${DBUSER}'@'${DB_HOST}'"

	echo OK
}

CREATE_DJANGO_USER(){

	# Create superuser
	LOGIN='gamemaster'
	MAIL='none@mail.com'
	PASS='pbkdf2_sha256$100000$jdNRfA8s4xZc$QS9LDv1ntYYWSO445RL1aVeTFWwLcU2cLMLyuy1G0Lc='
	DATE=$(date +"%Y-%m-%d %H:%M:%S.%6N")

	echo -n "[ * ] Creating Django superuser \`${LOGIN}\` (${MAIL})... "

	sudo mysql -u root -e "INSERT INTO auth_user VALUES(1,'${PASS}',NULL,1,'${LOGIN}','','','${MAIL}',1,1,'${DATE}')" "${DBNAME}"

	echo OK
}

MASTER(){

	CREATE_MYSQL_ROOT_CONFIG

	KILL_MYSQL_TASKS

	CREATE_MYSQL_DATABASE

	# Disable this line when reverse dns is enabled
	CREATE_MYSQL_USER %

	# Make migrations
	echo "[ * ] Running ${PYTHON} manage.py makemigrations..."
	${PYTHON} manage.py makemigrations

	# Migrate
	echo "[ * ] Running ${PYTHON} manage.py migrate..."
	${PYTHON} manage.py migrate

	CREATE_DJANGO_USER

	CREATE_MYSQL_CLIENT_CONFIG "${MASTER_HOSTNAME}"

	# Populate database
	echo "[ * ] Running ${PYTHON} manage.py populate-database..."
	${PYTHON} manage.py populate-database

	# Enable this loop to create a MySQL user for each Raspberry Pi
	#RASPIS=$(${PYTHON} manage.py shell < "${ROOTDIR}/scripts/show-remote-controllers.py")
	#for RASPI in $RASPIS; do
	#	CREATE_MYSQL_USER $RASPI
	#done
}


if [ $HOSTNAME == $MASTER_HOSTNAME ]; then
	MASTER
fi

CREATE_MYSQL_CLIENT_CONFIG "${MASTER_HOSTNAME}"
