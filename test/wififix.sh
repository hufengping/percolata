#!bin/bash

sleep 10

am start com.percolata.wififix/com.percolata.wififix.MainActivity

sleep 10

pm uninstall com.percolata.wififix

sleep 10

if [ -f "/data/misc/wifi/ipconfig.txt" ]
then
  rm /data/misc/wifi/ipconfig.txt
fi

reboot
rm -rf file