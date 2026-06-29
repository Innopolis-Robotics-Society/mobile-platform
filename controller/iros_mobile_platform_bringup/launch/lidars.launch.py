import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='lidar_wrapper',
            executable='sllidar_node',
            name='lidar_front',
            parameters=[{'channel_type': 'serial',
                         'hardware_id': 'lidar: front/.3',
                         'serial_port': '/dev/lidar_front', 
                         'serial_baudrate': 460800, 
                         'frame_id': 'lidar_front',
                         'inverted': False, 
                         'angle_compensate': True, 
                         'scan_mode': 'Standard'}],
            output='screen',
            remappings=[("/scan", "/laser_scan_front"), ("/stop_motor", "/laser_front_stop"), ("/start_motor", "/laser_front_start")]
        ),
        Node(
            package='lidar_wrapper',
            executable='sllidar_node',
            name='lidar_back',
            parameters=[{'channel_type': 'serial',
                         'hardware_id': 'lidar: back/.4',
                         'serial_port': '/dev/lidar_back', 
                         'serial_baudrate': 460800, 
                         'frame_id': 'lidar_back',
                         'inverted': False, 
                         'angle_compensate': True, 
                         'scan_mode': 'Standard'}],
            output='screen',
            remappings=[("/scan", "/laser_scan_back"), ("/stop_motor", "/laser_back_stop"), ("/start_motor", "/laser_back_start")]
        )
    ])

