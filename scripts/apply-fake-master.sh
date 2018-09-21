#!/bin/bash

. $(dirname $0)/env.sh

cd ${ROOTDIR}

patch -p1 < patches/fake-master.patch
