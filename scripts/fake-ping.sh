#!/bin/bash

. $(dirname $0)/env.sh

TEMP=$(mktemp)

echo -en "HTTP/1.1 200 OK\\r
Server: nginx\\r
Date: Wed, 19 Sep 2018 12:36:03 GMT\\r
Content-Type: text/html; charset=utf-8\\r
Content-Length: 2\\r
Connection: keep-alive\\r
Content-Language: en\\r
Vary: Origin\\r
X-Frame-Options: SAMEORIGIN\\r
\\r
OK" > ${TEMP}

echo "Stopping nginx (dont forget to run \`sudo /etc/init.d/nginx start\` when you're done!)..."
sudo /etc/init.d/nginx stop

while true; do

	echo "Listening on port 80..."
	sudo nc -l -p 80 < ${TEMP}

	sleep 1
done
