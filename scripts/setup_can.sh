#!/bin/bash

# Wait for can0 interface to become available
until ip link show can0 > /dev/null 2>&1
do
    sleep 1
done

# Initialize native SocketCAN interface
ip link set can0 type can bitrate 500000
ip link set can0 up
ip link set can0 txqueuelen 2000