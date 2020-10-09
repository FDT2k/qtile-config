#!/bin/bash

DIR=$(dirname $0)
$DIR/bin/theme/reload &

#telegram-desktop &
#thunderbird &
#bin/clickup &

synology-drive &

notify-send "autostart"

sleep 1

#feh --bg-fill ~/background.jpg &
