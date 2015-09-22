#!/system/bin/sh

x=0

while [ x -lt $1 ];do
    ifconfig wlan0 down
    sleep 1
    let x=x+1
done
