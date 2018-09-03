#!/bin/bash

HOSTS_FILE=/etc/hosts
HOSTNAME_FILE=/etc/hostname

HOSTNAME=$1
if [ -z "${HOSTNAME}" ]; then
	echo "Usage: $0 <hostname>"
	exit
fi

# Modify /etc/hostname to reflect the new hostname
echo -n "[ * ] Updating ${HOSTNAME_FILE} with new hostname \`${HOSTNAME}\`... "
sudo sh -c "echo ${HOSTNAME} > ${HOSTNAME_FILE}"
echo OK

# Modify /etc/hosts so we can resolve our own name locally
echo -n "[ * ] Updating ${HOSTS_FILE} with new hostname \`${HOSTNAME}\`... "
sudo sed -i "s/^127.0.1.1[^0-9].*$/127.0.1.1\t$HOSTNAME/" "${HOSTS_FILE}"
echo OK

#
echo -n "[ * ] Setting system hostname to \`${HOSTNAME}\`... "
sudo hostname "${HOSTNAME}"
echo OK

# Reconfigure avahi-daemon for the change to take effect
echo -n "[ * ] Restarting avahi-daemon for the change to take effect... "
sudo dpkg-reconfigure avahi-daemon
echo OK
