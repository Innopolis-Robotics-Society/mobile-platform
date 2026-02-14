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

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_slam = LaunchConfiguration("use_slam")
    map_file = LaunchConfiguration("map_file")

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )
    
    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="False"
    )
    
    map_file_arg = DeclareLaunchArgument(
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
            ("use_sim_time", use_sim_time),
        ],
    )

    # Sensor fusion launch
    sensor_fusion_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_sensor_fusion"),
                        "launch",
                        "sensor_fusion.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", use_sim_time),
        ],
    )
    
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_localization"),
                        "launch",
                        "global_localization.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", use_sim_time),
        ],
        condition=UnlessCondition(use_slam)
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_mapping"),
                        "launch",
                        "slam.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", use_sim_time),
        ],
        condition=IfCondition(use_slam)
    )

    # Path planner launch
    path_planner_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_path_planner"),
                        "launch",
                        "path_planner_nav2.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", use_sim_time),
            ("slam", use_slam),
            ("map_file", map_file),
        ],
    )

    return LaunchDescription(
        [
            use_sim_time_arg,
            use_slam_arg,
            map_file_arg,
            
            #launch lidar merge
            #TimerAction( period=1.0, actions=[merge_lidars]),
            merge_lidars,
            #Sensor fusion
            #TimerAction( period=3.0, actions=[sensor_fusion_launch]),
            sensor_fusion_launch,
            #Path planner
            #TimerAction( period=4.0, actions=[iros_mobile_platform_path_planner_launch]),
            path_planner_launch,
            localization,
            slam,
        ]
    )