#!/bin/bash

telegram-desktop &
thunderbird &
bin/clickup &

synology-drive &


sleep 1

feh --bg-fill ~/background.jpg &
bin/configure-dunst &