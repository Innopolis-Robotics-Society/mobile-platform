from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
import os
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # RViz node
    rviz_config_file = PathJoinSubstitution([FindPackageShare("overlord100"), "rviz", "sim_with_laser_merge.rviz"])
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="True",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )
    
    use_slam = LaunchConfiguration("use_slam")
    
    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="false"
    )
    
    map_file = DeclareLaunchArgument(
        "map_file",
        default_value="map.yaml",
    )

    # Simulation launch (starts immediately)
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("overlord100_simulation"),
                        "launch",
                        "simulation.launch.py",
                    ]
                )
            ]
        )
    )

    # Merging lidars (wait 3 seconds after simulation)
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

    # Controller launch (wait 6 seconds total - 3 secs after lidar merge)
    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("overlord100_bringup"),
                        "launch",
                        "only_sim_controller.launch.py",
                    ]
                )
            ]
        )
    )

    # Sensor fusion launch (wait 10 seconds total - 4 secs after controller)
    sensor_fusion_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("overlord100_sensor_fusion"),
                        "launch",
                        "sensor_fusion.launch.py",
                    ]
                )
            ]
        )
    )
    
    localization = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("overlord100_localization"),
            "launch",
            "global_localization.launch.py"
        ),
        condition=UnlessCondition(use_slam)
    )

    slam = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("overlord100_mapping"),
            "launch",
            "slam.launch.py"
        ),
        condition=IfCondition(use_slam)
    )

    # Path planner launch (wait 13 seconds total - 3 secs after sensor fusion)
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

    return LaunchDescription(
        [
            use_sim_time,
            use_slam_arg,
            map_file,
            
            # Launch simulation immediately
            sim_launch,
            
            # Wait 3 seconds, then launch lidar merge
            TimerAction(
                period=3.0,
                actions=[merge_lidars]
            ),
            
            # Wait 6 seconds total (3 more after lidar merge), then launch controller
            TimerAction(
                period=6.0,
                actions=[controller_launch]
            ),
            
            # Wait 10 seconds total (4 more after controller), then launch sensor fusion
            TimerAction(
                period=10.0,
                actions=[sensor_fusion_launch]
            ),
            
            # Wait 13 seconds total (3 more after sensor fusion), then launch path planner
            # TimerAction(
            #     period=13.0,
            #     actions=[path_planner_launch]
            # ),
            
            # Launch RViz immediately (or you can add a timer if you want it delayed)
            localization,
            slam,
            rviz_node,
            # Initialize starting pose
            # startPoseInit,
        ]
    )
