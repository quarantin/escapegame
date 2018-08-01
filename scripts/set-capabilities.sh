#!/bin/bash

. $(dirname $0)/env.sh

# Allows Python to bind privileged ports without having root privileges
sudo setcap 'cap_net_bind_service=+ep' "${PYTHON_BIN}"
