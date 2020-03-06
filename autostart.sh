#!/bin/bash

telegram-desktop &
thunderbird &
discord &

sleep 1
bash bin/last-layout >> ~/.config/qtile/layout.log

feh --bg-fill ~/background.jpg &
