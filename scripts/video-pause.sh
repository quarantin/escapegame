#!/bin/bash

. $(dirname $0)/env.sh

mkfifo $PLAYER_FIFO 2> /dev/null

echo pause > $PLAYER_FIFO
