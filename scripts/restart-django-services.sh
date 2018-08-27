#!/bin/bash

. $(dirname $0)/env.sh

sudo killall -9 ${PYTHON}
