#!/bin/bash

# Allows Python to bind port 80 without root privileges
sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3.5
