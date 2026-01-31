#!/bin/bash

source /opt/ros/humble/setup.bash && 
colcon build && 
source install/setup.bash &&
ros2 launch overlord100_simulation simulation.launch.py
