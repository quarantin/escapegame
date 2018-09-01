#!/bin/bash

. $(dirname $0)/env.sh

echo -n '[ * ] Restarting django services...'
sudo killall -9 ${PYTHON}
echo ' OK'
