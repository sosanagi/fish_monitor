#!/bin/bash

cd /home/pi/fish/dsp/

sleep 60

export DISPLAY=:0.0
#PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
#export PYTHONPATH="/usr/lib/python37.zip:/usr/lib/python3.7:/usr/lib/python3.7/lib-dynload:/home/pi/.local/lib/python3.7/site-packages:/usr/local/lib/python3.7/dist-packages:/usr/lib/python3/dist-packages"

python3 plot.py &
python3 dsp_fish.py
