#!/bin/sh

DIR=$(dirname $0)
SCR=$(basename $0)


#force refreshing plugged monitors
xrandr
xrandr --output eDP-1 --off --output HDMI-1 --primary --mode 3440x1440 --pos 0x0 --rotate normal

pushd $DIR/..

rm -f last-layout
ln -s monitor_layout/$SCR last-layout
#popd
