#!/bin/bash

HOST=127.0.0.1
JSON='{"username": "gamemaster","password": "gamemaster"}'

curl -X POST --data "${JSON}" "http://${HOST}/api/get-token/"

echo
