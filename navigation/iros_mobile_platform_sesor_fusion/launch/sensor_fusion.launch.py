from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
import os

def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")

    robot_localization = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[
            os.path.join(get_package_share_directory("iros_mobile_platform_sensor_fusion"), "config", "ekf2.yaml"),
            {"use_sim_time": use_sim_time},
                        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="False",
            description="Use simulation clock",
        ),
        robot_localization
    ])
