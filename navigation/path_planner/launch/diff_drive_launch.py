from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.substitutions import (
    Command,
    FindExecutable,
    PathJoinSubstitution,
    LaunchConfiguration,
)
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("path_planner"),
            "config",
            "diff_drive_params.yaml",
        ]
    )

    return LaunchDescription(
        [
            # Start ros2_control node with the URDF
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                name="ros2_control_node",
                output="screen",
                parameters=[robot_controllers],
            ),
            # Spawn the diff_drive_controller
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "diff_drive_controller",
                    "--controller-manager",
                    "/controller_manager",
                ],
                output="screen",
            ),
        ]
    )
