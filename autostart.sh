#!/bin/bash

DIR=$(dirname $0)
$DIR/bin/theme/reload &

#telegram-desktop &
#thunderbird &
#bin/clickup &
xss-lock -- $DIR/bin/i3lock-multimonitor/lock &

notify-send "autostart"

#tmux new -d -s ndb -c ~/Documents/work/fuge_workspaces "fuge shell microservice_dev/dev.yml"

sleep 1

#feh --bg-fill ~/background.jpg &
