# iros_mobile_platform Mobile Platform

This repository integrates hardware, frontend, and backend modules for the iros_mobile_platform Mobile Platform. The backend module consists of the following components:

1. **Controller**: Includes the high-level controller and various infrastructure packages such as the log collector and mode switcher.
2. **SLAM**: Provides Simultaneous Localization and Mapping functionalities.
3. **Path Planner**: Responsible for determining the optimal path.

## Installation & launch
### Docker

#### One-liner, simulator 
```docker
docker compose up --build simulator
```

#### Development, simulator
If you want to play around, you could launch the terminal:
```docker
docker compose up --build terminal
```

You can attach to the docker from other terminals, by running:
```docker
docker compose exec terminal bash
```

Inside there, you have to build the project manually:
```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
ros2 launch iros_mobile_platform sim.launch.py
```

#### SLAM, simulator

To start mapping, set launch argument `run_mapping` for `sim.launch.py` to `True`:
```bash
ros2 launch iros_mobile_platform sim.launch.py run_mapping:=True
```


To save the map, enter the following command in the new terminal:
```bash
source /opt/ros/humble/setup.bash
ros2 run nav2_map_server map_saver_cli -f <new_map_name>
```
> **_NOTE:_** The save path can be specified as `<path_to_map>/<new_map_name>` or run the command in the desired directory

To use a specific map for SLAM in simulator, provide map file to the launch argument `map_file` for `sim.launch.py`:
```bash
ros2 launch iros_mobile_platform sim.launch.py map_file:=<map_file>
```
> **_NOTE:_** The map file is expected in the directory `/iros_mobile_platform/maps`

#### Launching hardware
TBD

### Local installation
#### Dependencies 
The project software is developed using the ROS2 Humble middleware and relies on the following external dependencies:

1. [Slam Toolbox](https://github.com/SteveMacenski/slam_toolbox)
2. [Nav2](https://github.com/ros-navigation/navigation2)

Additionally, the following ROS2 package is used for hardware components:

3. [Sllidar](https://github.com/Slamtec/sllidar_ros2)

They could be installed at:
```bash
RUN apt-get install -y ros-humble-slam-toolbox ros-humble-navigation2 ros-humble-nav2-bringup 
```

#### Launching simulator
```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
ros2 launch iros_mobile_platform sim.launch.py
```
#### Launching hardware
TBD
