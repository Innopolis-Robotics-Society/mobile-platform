from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    socketcan = Node(
        package="ros2socketcan_bridge",
        executable="ros2socketcan",
        name="ros2socketcan",
        output="log",
        arguments=['--ros-args', '--log-level', 'fatal'],
    )
    # Start motor_driver node
    motor_driver = Node(
        package="overlord100_motors",
        executable="motors_driver_node",
        name="motors_driver_node",
        output="screen",
    )
    # motor encoders
    encoders_node = Node(
        package="overlord100_motors",
        executable="encoders_node",
        name="encoders_node",
        output="screen"
    )

    return LaunchDescription([socketcan, encoders_node, motor_driver])
