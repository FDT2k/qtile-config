#!/bin/bash

telegram-desktop &
thunderbird &
bin/clickup &

sleep 1
bash bin/last-layout >> ~/.config/qtile/layout.log

feh --bg-fill ~/background.jpg &
