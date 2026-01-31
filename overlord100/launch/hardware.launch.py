from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # RViz node
    rviz_config_file = PathJoinSubstitution([FindPackageShare("overlord100"), "rviz", "hardware.rviz"])
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
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

    # Models launch
    robot_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("overlord100_description"),
                        "launch",
                        "robot_state_publisher.launch.py",
                    ]
                )
            ]
        )
    )



    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("overlord100_description"),
                        "launch",
                        "etogo_net_i_ne_budet.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[],
    )
    socketcan = Node(
        package="ros2socketcan_bridge",
        executable="ros2socketcan",
        name="ros2socketcan",
        output="log",
        arguments=['--ros-args', '--log-level', 'fatal'],
    )
    # Start motor_driver node
    motor_driver = Node(
        package="overlord100_motors",
        executable="motors_driver_node",
        name="motors_driver_node",
        output="screen",
    )
    # Start IMU node
    imu_node = Node(
        package="jy901s_imu_ros2",
        executable="jy901s_imu_node",
        name="imu_node",
        output="screen",
    )
    # motor encoders
    encoders_node = Node(
        package="overlord100_motors",
        executable="encoders_node",
        name="encoders_node",
        output="screen"
    )
    # Launch lidars
    lidars_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                FindPackageShare("overlord100_bringup"),
                "/launch",
                "/lidars.launch.py",
            ]
        )
    )
    # Start battery_node
    battery_node = Node(
        package="overlord100_battery",
        executable="battery_monitor",
        name="battery_monitor",
        output="screen",
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
            ("use_sim_time", "False"),
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
            run_mapping,
            map_file,
            robot_description,
            # Launch the hardware components
            lidars_launch,
            socketcan,
            encoders_node,
            motor_driver,
            battery_node,
            imu_node,
            # Launch the controller
            controller_launch,
            # Launch the path planner
            #slam_launch,
            path_planner_launch,
            # Merge two laserscans together
            merge_lidars,
            # Finally launch RViz
            rviz_node,
        ]
    )
