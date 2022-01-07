#!/bin/bash
screen=$1
value=$(echo "" | rofi -dmenu -p "Enter brightness  (float) > "  -theme-str 'listview { enabled: false;}' ); 
xrandr --output $screen --brightness $value