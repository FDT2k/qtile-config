#!/bin/bash
bash bin/last-layout

telegram-desktop &
thunderbird &
discord &

sleep 5

feh --bg-fill ~/background.jpg &
