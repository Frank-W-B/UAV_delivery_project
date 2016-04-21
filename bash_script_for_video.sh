#!/bin/bash
clear
echo "This is information provided by mysystem.sh. Program starts now."

echo "Hello, $USER"
echo

COUNTER=0
while [  $COUNTER -lt 54 ]; do
    echo The counter is $COUNTER
    python gmap_final.py
    firefox output.html
    shutter -d 3 --window=.*firefox.* -e
    wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded
    let COUNTER=COUNTER+1 
done

echo "Finished"
