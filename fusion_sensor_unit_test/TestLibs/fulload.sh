#!/system/bin/sh
cpuConsumingFunc()
{
    dd if = /dev / urandom | bzip2 - 9 >> /dev / null
}
fulload()
{
    x = 0
    while [ $x - lt $1 ]
    do
    cpuConsumingFunc &
    let x = x + 1
    done
}
echo "----- Starting CPU load"
fulload $1
echo "Press enter to stop CPU load"
read
echo "----- CPU load stopped"
killall dd
