export PATH=/sbin:/system/sbin:/system/bin:/system/xbin
sdcard=/sdcard
if [ ! -d /data/local/bin ]; then
    busybox mkdir -p /data/local/bin
fi
busybox cp ${sdcard}/fusion-sensor-mon.sh /data/local/bin
busybox chmod 755 /data/local/bin/fusion-sensor-mon.sh
busybox cp ${sdcard}/userinit.sh /data/local
busybox chmod 755 /data/local/userinit.sh
sync

