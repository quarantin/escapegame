#!/bin/bash

. $(dirname $0)/env.sh

echo -n '[ * ] Restarting django services...'
sudo kill -9 $(pidof ${PYTHON})
echo ' OK'
