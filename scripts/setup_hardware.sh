#!/bin/bash

# setup lidars and symlinks for them
echo "SUBSYSTEM==\"tty\",SUBSYSTEMS==\"usb\",DRIVERS==\"usb\",MODE:=\"0777\",SYMLINK+=\"usb_%s{devpath}\"" > /etc/udev/rules.d/99-rplidar_c1.rules
# setup CAN device and symlink for it
echo "SUBSYSTEM==\"tty\",SUBSYSTEMS==\"usb\",ATTRS{idProduct}==\"60c4\",SYMLINK+=\"CANable\"" > /etc/udev/rules.d/99-canable.rules
# setup battery sensor
echo "KERNEL==\"i2c-8\",SUBSYSTEM==\"i2c-dev\",MODE:=\"0777\"" > /etc/udev/rules.d/99-bat.rules
# setup IMU
echo "KERNEL==\"ttyTHS0\",SUBSYSTEM==\"tty\",MODE:=\"0777\"" > /etc/udev/rules.d/99-imu.rules
udevadm control --reload-rules
udevadm trigger

# setup CAN interface (will go up next reboot)
cp ./setup_can.sh /usr/sbin/overlord_setup_can.sh
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
