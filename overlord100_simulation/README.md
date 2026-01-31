### how to run

1. `ros2 launch overlord100_simulation gazebo.launch.py`
  1.1 or this also works: "ros2 launch overlord100_simulation gazebo.launch.py world_name:="clear_world"
2.  `ros2 launch overlord100_controller controller.launch.py `
3. `ros2 topic pub /overlord100_controller/cmd_vel geometry_msgs/msg/TwistStamped "header:
  stamp:
    sec: 0
    nanosec: 0
  frame_id: ''
twist:
  linear:
    x: 1.0
    y: 0.0
    z: 0.0
  angular:
    x: 0.0
    y: 0.0
    z: 3.0" 
`
  3.1 now robot can be controller by rqt_steering
4. works both in gazebo and rviz
5. so far, only DiffDrive controller (from ros2_control) is used, without assuming our custom controller.
   * If we use custom controller, we need to also make a odom publisher

So far, topics
```
/clicked_point
/clock
/color_camera
/depth_camera/points
/depth_camera_info
/dynamic_joint_states
/goal_pose
/imu/out
/initialpose
/joint_state_broadcaster/transition_event
/joint_states
/laser_scan_back
/laser_scan_front
/left_wheel
/model/overlord100/pose
/odom
/overlord100_controller/cmd_vel_out
/overlord100_controller/cmd_vel_unstamped
/overlord100_controller/odom
/overlord100_controller/transition_event
/parameter_events
/regular_driver
/right_wheel
/robot_description
/rosout
/sonar_1_scan
/sonar_2_scan
/sonar_3_scan
/sonar_4_scan
/sonar_5_scan
/sonar_6_scan
/sonar_7_scan
/sonar_8_scan
/tf
/tf_static
```
and [rqt_graph](https://drive.google.com/file/d/1DCm7xx1aPz7fuxJEpUHQ_RFq6Iv8JryL/view?usp=sharing)

* Things to remember:
  * in controller config `use_time_stamped`
  * fix laser scans, camera, sonars, they are not working for now

