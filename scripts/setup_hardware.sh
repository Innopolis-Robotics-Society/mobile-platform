#!/bin/bash

# setup lidars and symlinks for them based on unique serial numbers
# WARNING: If front and back lidars are flipped in ROS, just swap "LIDAR" and "0001" below.
echo "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"10c4\", ATTRS{idProduct}==\"ea60\", ATTRS{serial}==\"LIDAR\", MODE=\"0666\", SYMLINK+=\"lidar_front\"" > /etc/udev/rules.d/99-lidars.rules
echo "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"10c4\", ATTRS{idProduct}==\"ea60\", ATTRS{serial}==\"0001\", MODE=\"0666\", SYMLINK+=\"lidar_back\"" >> /etc/udev/rules.d/99-lidars.rules

# setup battery sensor
echo "KERNEL==\"i2c-8\",SUBSYSTEM==\"i2c-dev\",MODE:=\"0777\"" > /etc/udev/rules.d/99-bat.rules
# setup IMU
echo "KERNEL==\"ttyTHS0\",SUBSYSTEM==\"tty\",MODE:=\"0777\"" > /etc/udev/rules.d/99-imu.rules
udevadm control --reload-rules
udevadm trigger

# setup CAN interface (will go up next reboot)
cp "$(dirname "$0")/setup_can.sh" /usr/sbin/overlord_setup_can.sh
sed -i '/setup_can.sh/d' /etc/crontab
echo "@reboot root /usr/sbin/overlord_setup_can.sh" >> /etc/crontab
# disable dynamic cpu freq management (will go up next reboot)
sed -i '/nvpmodel/d' /etc/crontab
echo "@reboot root /usr/sbin/nvpmodel -m 8 && /usr/bin/jetson_clocks" >> /etc/crontab


read -p "Reboot [y/N]? " -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    reboot
fi
