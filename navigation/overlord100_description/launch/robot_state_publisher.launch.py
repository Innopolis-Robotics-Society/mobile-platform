import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )

    des_file = os.path.join(
        get_package_share_directory("overlord100_description"),
        "description",
        "overlord100.urdf.xacro",
    )

    robot_description = xacro.process(des_file)  # Process the xacro file directly

    return LaunchDescription(
        [
            use_sim_time,
            Node(
                package="overlord100_description",
                executable="cmd_to_odom",
                name="cmd_to_odom",
                output="screen",
                parameters=[
                    {}
                ],
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "use_sim_time": LaunchConfiguration("use_sim_time"),
                        "robot_description": robot_description,
                    }
                ],
            ),
        ]
    )
