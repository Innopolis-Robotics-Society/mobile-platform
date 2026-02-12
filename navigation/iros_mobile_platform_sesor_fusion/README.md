* now, we have a working initialization of `ekf_node`, but it is very noisy
* what is set_pose topic what `ekf_node` is subscribed
* think about exactly which data from odom, imu you need to use: `x_pos`, `acel_z`, `vel_z`...


* Apr 26,
  * when launching `sensor fusion` and `controller` at the same time, peale disable `controller` for publishing `odom tf`. otherwise `sensor fusion` and `controller` simultaneously publish to `odom_tf`, thus making robot jump in rviz
