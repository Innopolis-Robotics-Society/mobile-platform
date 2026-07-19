#
#   created by: Michael Jonathan (mich1342)
#   github.com/mich1342
#   24/2/2022
#
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
import launch_ros.actions
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    # TODO: replace back with relative path
    # config = os.path.join(
    #     get_package_share_directory("ros2_laser_scan_merger"), "config", "params.yaml"
    # )
    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false", #TO-DO
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )

    config = PathJoinSubstitution(
        [
            FindPackageShare("ros2_laser_scan_merger"),
            "config",
            "params.yaml",
        ]
    )

    laser_filter_config = PathJoinSubstitution(
        [
            FindPackageShare("ros2_laser_scan_merger"),
            "config",
            "laser_filter_params.yaml",
        ]
    )
    return LaunchDescription(
        [
            use_sim_time,
            launch_ros.actions.Node(
                package="ros2_laser_scan_merger",
                executable="ros2_laser_scan_merger",
                parameters=[config, {"use_sim_time": LaunchConfiguration("use_sim_time")}],
                output="screen",
                respawn=True,
                respawn_delay=2,
            ),

            launch_ros.actions.Node(
                name="pointcloud_to_laserscan",
                package="pointcloud_to_laserscan",
                executable="pointcloud_to_laserscan_node",
                parameters=[config, {"use_sim_time": LaunchConfiguration("use_sim_time")}],
                remappings=[("scan", "scan_raw")],
            ),

	    launch_ros.actions.Node(
                package="laser_filters",
                executable="scan_to_scan_filter_chain",
                parameters=[laser_filter_config, {"use_sim_time": LaunchConfiguration("use_sim_time")}],
                remappings=[
                    ("scan", "scan_raw"),
                    ("scan_filtered", "scan"),
                ],
                output="screen",
            ),
        ]
    )
