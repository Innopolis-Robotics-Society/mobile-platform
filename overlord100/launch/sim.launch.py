from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # RViz node
    rviz_config_file = PathJoinSubstitution([FindPackageShare("overlord100"), "rviz", "sim.rviz"])
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )
    run_mapping = DeclareLaunchArgument(
        "run_mapping",
        default_value="False",
        description="If True, the mapping is launched, which builds the map from scratch",
    )
    map_file = DeclareLaunchArgument(
        "map_file",
        default_value="map.yaml",
    )
    # Merging lidars
    merge_lidars = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("ros2_laser_scan_merger"),
                        "launch",
                        "merge_2_scan.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", LaunchConfiguration("use_sim_time")),
        ],
    )
    # TODO: why simulator launcher is in diff_drive_control.launch.py
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("overlord100_simulation"),
                        "launch",
                        "diff_drive_control.launch.py",
                    ]
                )
            ]
        )
    )

    path_planner_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("path_planner"),
                        "launch",
                        "path_planner_nav2.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", LaunchConfiguration("use_sim_time")),
            ("slam", LaunchConfiguration("run_mapping")),
            ("map_file", LaunchConfiguration("map_file")),
        ],
    )

    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("overlord100_bringup"),
                        "launch",
                        "simulator_control.launch.py",
                    ]
                )
            ]
        )
    )

    return LaunchDescription(
        [
            use_sim_time,
            run_mapping,
            map_file,
            # Launch the main simulation
            sim_launch,
            # Launch the controller
            controller_launch,
            # Launch the path planner
            path_planner_launch,
            # Merge two laserscans together
            merge_lidars,
            # Finally launch RViz
            rviz_node,
        ]
    )
