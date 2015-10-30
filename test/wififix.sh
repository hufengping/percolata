#!bin/bash

sleep 10

pm install wififix.apk                                           
                                                                 
am start com.percolata.wififix/com.percolata.wififix.MainActivity
         
sleep 180                         

am force-stop com.percolata.wififix 
                                  
pm uninstall com.percolata.wififix
        
sleep 10                                
                                        
if [ -f "/data/misc/wifi/ipconfig.txt" ]
then                             
  rm /data/misc/wifi/ipconfig.txt
fi    

rm -rf $0 
        
reboot   