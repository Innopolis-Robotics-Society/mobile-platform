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
        default_value="True",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )

    config = PathJoinSubstitution(
        [
            FindPackageShare("ros2_laser_scan_merger"),
            "config",
            "params.yaml",
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
            # TF2 for laser to map frame id, optional
            # launch_ros.actions.Node(
            #     package='tf2_ros',
            #     executable='static_transform_publisher',
            #     name='static_transform_publisher',
            #     arguments=[
            #         '--x', '0', '--y', '0', '--z', '0',
            #         '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
            #         '--frame-id', 'map', '--child-frame-id', 'laser'
            #     ]
            # ),
            # Call pointcloud_to_laserscan package
            launch_ros.actions.Node(
                name="pointcloud_to_laserscan",
                package="pointcloud_to_laserscan",
                executable="pointcloud_to_laserscan_node",
                parameters=[config, {"use_sim_time": LaunchConfiguration("use_sim_time")}],
            ),
        ]
    )
