# Hardware Module
This repository contains the hardware interface modules for the iros_mobile_platform_v2.0 project, including battery monitoring, motor control, and LiDAR integration.

## Battery Monitoring
The `battery_monitor.cpp` handles battery voltage measurement using the ADS1115 ADC and publishes the data as a ROS 2 BatteryState message.

- I2C Communication: Connects to the ADS1115 via I2C.
- Voltage Measurement: Converts voltage to percentage.
- ROS 2 Topic: Publishes on /battery_state.

## Motor Control
The `motors_driver_node.cpp` manages motor commands, converting velocity data into CAN bus messages.

- CAN Bus: Communicates with motor controllers.
- Velocity Control: Converts WheelsData to motor commands.
- ROS 2 Topics:
    - Subscribes: /wheels_control
    - Publishes: /CAN/can0/transmit

## Dependencies
- `ros2socketcan_bridge:` ROS 2 and SocketCAN bridge.
- `sllidar_ros2:` For integrating Slamtec LiDAR sensors.

## Run 

ros2 launch sllidar_ros2 sllidar_c1_launch.py
ros2 run ros2socketcan_bridge ros2socketcan
ros2 run zlac8015d motors_driver_node
ros2 run ads1115 battery_monitor

## Usage
Battery Monitoring: 
`ros2 topic echo /battery_state`

Motor Control: 
`ros2 topic pub /wheels_control iros_mobile_platform_msgs/msg/WheelsData "{left: 100, right: 100}"`
