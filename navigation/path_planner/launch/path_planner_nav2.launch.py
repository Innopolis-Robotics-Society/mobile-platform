from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node  # Add this import


def generate_launch_description():
    declare_slam_cmd = DeclareLaunchArgument(
        "slam",
        default_value="False",
        description="Whether run a SLAM",
    )
    declare_autostart_cmd = DeclareLaunchArgument(
        "autostart",
        default_value="True",
        description="Automatically startup the nav2 stack",
    )
    param_file = DeclareLaunchArgument(
        "params_file",
        default_value=PathJoinSubstitution(
            [
                FindPackageShare("path_planner"),
                "config",
                "nav2_params.yaml",
            ]
        ),
    )
    map_file = DeclareLaunchArgument(
        "map_file",
        default_value="map.yaml",
    )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time", default_value="False", description="Use simulation (Gazebo) clock if true"
    )

    # Path to the map file
    map = PathJoinSubstitution(
        [
            FindPackageShare("overlord100"),
            "maps",
            LaunchConfiguration("map_file"),
        ]
    )

    nav2_bringup_launch = IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare("nav2_bringup"), "launch", "bringup_launch.py"]),
        launch_arguments=[
            ("use_sim_time", LaunchConfiguration("use_sim_time")),
            ("params_file", LaunchConfiguration("params_file")),
            ("map", map),
            ("slam", LaunchConfiguration("slam")),
            ("autostart", LaunchConfiguration("autostart")),
        ],
    )

    ld = LaunchDescription(
        [
            declare_use_sim_time_cmd,
            declare_autostart_cmd,
            declare_slam_cmd,
            param_file,
            map_file,
            nav2_bringup_launch,
        ]
    )

    return ld
