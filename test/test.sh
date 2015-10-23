#!/bin/bash


if [ -f "/home/fengpinghu/Desktop/1.txt" ] 
then
  rm "/home/fengpinghu/Desktop/1.txt"
  echo "rm seccussful"
fi

for loop in 1 2 3 4 5
  do
    sleep 1
    echo "++++++++++"
    echo -e "\a"
  done
#rm $0
