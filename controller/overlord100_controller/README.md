# Overlord100-controller
Controller submodule

**Package `overlord100_controller`.**

`diff_drive_controller` is a ROS2 node designed to control a differential drive robot. 

## Module structure 

`cmd_vel_publisher` and `controller_subscriber` (inside `cmd_vel_publisher.cpp` and `controller_subscriber.cpp`) are temporary nodes to test the controller (inside `controller.cpp`).

*cmd_vel_publisher (`cmd_vel_publisher.cpp`) sends `Twist` over the topic `cmd_vel` to the overlord100_controller (`controller.cpp`). And the controller sends `WheelData` to the controller_subscriber (`controller_subscriber.cpp`) over the topic `wheels_control`*


## Features

- Subscribes to the `cmd_vel` topic (with the assumption that `cmd_vel` measurements unit is m/s).
- Publishes (angular) wheel velocities (in rpm) to the `wheels_control` topic.
- Uses parameters for platform base wheel radius (the robot's geometry).

### Topics 

**Subscribed**

- `/cmd_vel` (`geometry_msgs/msg/Twist`): Subscribes to the velocity command messages, which contain linear and angular velocities. 

- `/wheels_control` (`overlord100_msgs/msg/WheelsData`): Publishes the calculated wheel velocities to control the robot. 

**Published** 

### How to run the node:

Run in separate terminals the following commands. Do not forget to source ros2.

```ros2 run overlord100_controller cmd_vel_publisher```
```ros2 run overlord100_controller diff_drive_controller```
```ros2 run overlord100_controller controller_subscriber```