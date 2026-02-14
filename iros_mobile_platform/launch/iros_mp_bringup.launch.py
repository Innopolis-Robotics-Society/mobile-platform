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
    use_slam = LaunchConfiguration("use_slam")
    rviz_config = LaunchConfiguration("rviz_config")
    map_file = LaunchConfiguration("map_file")
    use_sim = LaunchConfiguration("use_sim_time")

    rviz_config_arg = DeclareLaunchArgument(
        "rviz_config",
        default_value=PathJoinSubstitution([FindPackageShare("iros_mobile_platform"), "rviz", "sim_with_laser_merge.rviz"]),
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )

    use_sim_arg = DeclareLaunchArgument(
        "use_sim",
        default_value="True",
        description="Use simulation (Gazebo) if launch argument is 'True'",
    )

    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="False"
    )

    map_file_arg = DeclareLaunchArgument(
        "map_file",
        default_value="map.yaml",
    )


    # Simulation launch
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_simulation"),
                        "launch",
                        "simulation.launch.py",
                    ]
                )
            ]
        )
    )

    # Controller launch
    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_bringup"),
                        "launch",
                        "only_sim_controller.launch.py",
                    ]
                )
            ]
        )
    )

    # IRoS nav stack
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform"),
                        "launch",
                        "common",
                        "navigation.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", use_sim_time),
            ("use_slam", use_slam),
            ("map_file", map_file),
        ],
    )

    # RViz node
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config],
        parameters=[{"use_sim_time": use_sim_time}],
    )


    return LaunchDescription(
        [
            use_sim_time_arg,
            use_slam_arg,
            map_file_arg,
            rviz_config_arg,
            
            # Launch simulation
            sim_launch,
            #TimerAction(period=2.0, actions=[controller_launch]),
            controller_launch,
            navigation,
            # Launch RViz
            rviz_node,

            #startPoseInit, #TO-DO
        ]
    )
