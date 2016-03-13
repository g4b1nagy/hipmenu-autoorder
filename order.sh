#!/bin/sh

cd /home/pi/hipmenu-autoorder
source venv/bin/activate
python -u order.py >> order.log
