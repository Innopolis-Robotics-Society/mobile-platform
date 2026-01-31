# Controller module
Controller module implements the high-level control over the robot. This module includes the following functional packages:


- overlord100_controller that recalculates the velocity of the platform's center into wheels velocities,

- overlord100_switcher that implements switching between manual and autonomous modes,

- overlord100_logger that collects all the log messages for further transfer to the frontend module,

- overlord100_bringup contains the core file for launching the whole software stack for the robot.

For launching on the hardware use this command:

```ros2 launch overlord100_bringup hardware_control.launch.py```

For launching on with simulation use this command:

```ros2 launch overlord100_bringup simulation_control.launch.py```

*Note that the controller module also contains `manual_control.launch.py`, which will be obsolete soon: it will be substitutes by 2 separate launchers: `hardware_control.launch.py` and `simulation_control.launch.py`. However, they are under development yet.*
