#!/bin/bash

until ls /dev/CAN* | grep -q 'CANable'
do
    sleep 1
done
sudo slcand -o -c -s6 /dev/CANable can0
sudo ifconfig can0 up
sudo ifconfig can0 txqueuelen 2000
