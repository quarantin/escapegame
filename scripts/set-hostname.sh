#!/bin/bash

HOSTS_FILE=/etc/hosts
HOSTNAME_FILE=/etc/hostname
OLD_HOSTNAME=$(hostname)

HOSTNAME=$1
if [ -z "${HOSTNAME}" ]; then
	echo "Usage: $0 <hostname>"
	exit
fi

if [ ${HOSTNAME} = ${OLD_HOSTNAME} ]; then
	echo 'Not changing same hostname'
	exit
fi

# Ask sudo password before anything else to avoid polluting script output.
sudo echo -n > /dev/null

# Modify /etc/hosts so we can resolve both our old and new hostnames locally
# This allow us to avoid the error sudo: Unable to resolve host <old hostname>
sudo sed -i "s/^127.0.1.1[^0-9].*$/127.0.1.1\t${HOSTNAME} ${OLD_HOSTNAME}/" ${HOSTS_FILE}

# Modify /etc/hostname to reflect the new hostname
echo -n "[ * ] Updating ${HOSTNAME_FILE} with new hostname \`${HOSTNAME}\`... "
sudo sh -c "echo ${HOSTNAME} > ${HOSTNAME_FILE}"
echo OK

#
echo -n "[ * ] Setting system hostname to \`${HOSTNAME}\`... "
sudo hostname "${HOSTNAME}"
echo OK

# Reconfigure avahi-daemon for the change to take effect
echo -n "[ * ] Restarting avahi-daemon for the change to take effect... "
sudo dpkg-reconfigure avahi-daemon
echo OK

# Modify /etc/hosts to remove old hostname
echo -n "[ * ] Updating ${HOSTS_FILE} with new hostname \`${HOSTNAME}\`... "
sudo sed -i "s/^127.0.1.1[^0-9].*$/127.0.1.1\t$HOSTNAME/" ${HOSTS_FILE}
echo OK
