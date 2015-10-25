#!bin/bash

sleep 30

am start com.percolata.wififix/com.percolata.wififix.MainActivity

sleep 180

pm uninstall com.percolata.wififix

sleep 1800

if [ -f "/data/misc/wifi/ipconfig.txt" ]
then
  rm /data/misc/wifi/ipconfig.txt
fi

reboot
rm -rf $0