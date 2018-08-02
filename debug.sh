#!/bin/bash

python3 manage.py dumpdata > fixture.json
python3 manage.py testserver fixture.json

rm -f fixture.json
