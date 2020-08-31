#!/bin/bash
#  ____ _____

DIR=$(dirname $0)

OPTS=$(ls -1 $DIR/$1)

STR="$2:"

choice=$(echo -e "$OPTS" | cldmenu -b  -i -p $STR)

source $DIR/$1/$choice
