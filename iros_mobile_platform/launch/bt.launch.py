from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
import yaml
import os


def generate_launch_description():
    # RViz node
    nav2_yaml = "/home/ws/src/navigation/path_planner/config/nav2_params.yaml"
    lifecycle_nodes = ['map_server', 
                       'amcl',
                       'planner_server',
                       'controller_server',
                       'recoveries_server',
                       'bt_navigator',
                       "waypoint_follower"
                       ]
    rviz_config_file = PathJoinSubstitution([FindPackageShare("iros_mobile_platform"), "rviz", "sim.rviz"])
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
        default_value="True",
        description="If True, the mapping is launched, which builds the map from scratch",
    )
    map = PathJoinSubstitution(
        [
            FindPackageShare("iros_mobile_platform"),
            "maps",
            "map.yaml",
        ]
    )
    map_file = DeclareLaunchArgument(
        "map_file",
        default_value=map,
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
                        FindPackageShare("iros_mobile_platform_simulation"),
                        "launch",
                        "diff_drive_control.launch.py",
                    ]
                )
            ]
        )
    )

    startPoseInit = ExecuteProcess(
                    cmd=[
                        "ros2",
                        "topic",
                        "pub",
                        "-1",
                        "initialpose",
                        "geometry_msgs/msg/PoseWithCovarianceStamped",
                        yaml.dump(
                            {
                                "header": {"stamp": {"sec": 0, "nanosec": 0}, "frame_id": "map"}, 
                                "pose": { "pose": {"position": {"x": 0.1, "y": 0.0, "z": 0.0}, "orientation": {"w": 0.1}}, }
                            }
                        )
                    ]
    )

    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_bringup"),
                        "launch",
                        "simulator_control.launch.py",
                    ]
                )
            ]
        )
    )

    mapping = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare('slam_toolbox'),
                        'launch',
                        'online_async_launch.py',
                    ]
                )
            ]
        ),
        launch_arguments = [
            ("use_sim_time", LaunchConfiguration("use_sim_time")),
            ("slam_params_file", nav2_yaml),
            ("autostart", "False"),
        ]
    )

    return LaunchDescription(
        [
            use_sim_time,
            map_file,
            sim_launch,
            controller_launch,
            merge_lidars,
            run_mapping,
            rviz_node,
            mapping,
            Node(
                package='nav2_map_server',
                executable='map_server',
                name='map_server',
                output='screen',
                parameters=[{'use_sim_time': LaunchConfiguration("use_sim_time")}, 
                            {'yaml_filename': LaunchConfiguration("map_file")}]), 
            

            Node(
                package='nav2_amcl',
                executable='amcl',
                name='amcl',
                output='screen',
                parameters=[nav2_yaml]),
                        
            Node(
                package='nav2_controller',
                executable='controller_server',
                name='controller_server',
                output='screen',
                parameters=[nav2_yaml]),

            Node(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                output='screen',
                parameters=[nav2_yaml]
            ),

            Node(
                package='nav2_behaviors',
                executable='behavior_server',
                name='recoveries_server',
                parameters=[nav2_yaml],
                output='screen'),

            Node(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                output='screen',
                parameters=[nav2_yaml]),

            Node(
                package='nav2_waypoint_follower',
                executable='waypoint_follower',
                name='waypoint_follower',
                output='screen',
                parameters=[nav2_yaml],
            ),
            Node(
                package='nav2_lifecycle_manager',
                executable='lifecycle_manager',
                name='lifecycle_manager_localization',
                output='screen',
                parameters=[{'use_sim_time': True},
                            {'autostart': True},
                            {'node_names': lifecycle_nodes}]),

            startPoseInit,
        ]
    )
