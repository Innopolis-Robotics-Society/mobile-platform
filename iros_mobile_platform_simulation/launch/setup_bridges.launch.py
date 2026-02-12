import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():

    # Bridge
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            # "/laser_scan_back@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/laser_scan_front@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_1_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_2_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_3_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_4_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_5_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_6_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_7_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/sonar_8_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            # "/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo",
            # "/color_camera@sensor_msgs/msg/Image[ignition.msgs.Image",
            # "/depth_camera@sensor_msgs/msg/Image[ignition.msgs.Image",
            # "/depth_camera/points@sensor_msgs/msg/PointCloud2[ignition.msgs.PointCloudPacked",
            # "/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU",
            # "/regular_driver@geometry_msgs/msg/Twist@ignition.msgs.Twist",
            # "/world/mvp_world/model/iros_mobile_platform/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model",
            # "/model/iros_mobile_platform/pose@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            # "/odom/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            # "/model/iros_mobile_platform/joint/chassis_to_left_wheel/cmd_vel@std_msgs/msg/Float64@ignition.msgs.Double",
            # "/model/iros_mobile_platform/joint/chassis_to_right_wheel/cmd_vel@std_msgs/msg/Float64@ignition.msgs.Double",
            # "/odom@nav_msgs/msg/Odometry[ignition.msgs.OdometryWithCovariance",
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",
            "/laser_scan_back@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/laser_scan_front@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
        ],
        remappings=[
            # ("/odom/tf", "/tf"),
            ("/world/mvp_world/model/iros_mobile_platform/joint_state", "/joint_states"),
            # ("/camera_info", "/depth_camera_info"),
            # ("/model/iros_mobile_platform/joint/chassis_to_left_wheel/cmd_vel", "/left_wheel"),
            # ("/model/iros_mobile_platform/joint/chassis_to_right_wheel/cmd_vel", "/right_wheel"),
            ("/imu", "/imu/out")
        ],
        output="screen",
    )

    return LaunchDescription([bridge])
