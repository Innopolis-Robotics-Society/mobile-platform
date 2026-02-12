from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument

def generate_launch_description():

    ros2_controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_controller"), "launch"),
                "/controller.launch.py",
            ]
        )
    )
    
    cmd_vel_relay = Node(
        package="topic_tools",
        executable="relay",
        arguments=["/cmd_vel", "/overlord100_controller/cmd_vel_unstamped"],
        output="screen",
    )

    rqt_node_with_ros2_controller = Node(
        package="rqt_robot_steering",
        executable="rqt_robot_steering",
        remappings=[
        ],
    )
    return LaunchDescription(
        [
            # Start log_collector node
            ros2_controller,
            cmd_vel_relay,
            rqt_node_with_ros2_controller,
        ]
    )