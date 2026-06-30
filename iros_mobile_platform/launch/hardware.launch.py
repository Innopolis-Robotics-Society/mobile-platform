from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # RViz node
    rviz_config_file = PathJoinSubstitution([FindPackageShare("iros_mobile_platform"), "rviz", "hardware.rviz"])
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
    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
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
                        FindPackageShare("iros_mobile_platform_description"),
                        "launch",
                        "robot_state_publisher.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments=[
            ("use_sim_time", LaunchConfiguration("use_sim_time")),
            ("publish_tf", "false")
        ],
    )



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
            ("use_sim_time", LaunchConfiguration("use_sim_time")),
        ],
    )
    
    encoders_to_odom_node = Node(
        package="iros_mobile_platform_controller",
        executable="encoders_to_odom",
        name="encoders_to_odom",
        output="screen",
        parameters=[
            {"publish_tf": LaunchConfiguration("publish_tf", default="false")}
        ],
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
        package="iros_mobile_platform_motors",
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
        parameters=[{"port": "/dev/ttyTHS0", "baudrate": 38400}],
    )
    # motor encoders
    encoders_node = Node(
        package="iros_mobile_platform_motors",
        executable="encoders_node",
        name="encoders_node",
        output="screen"
    )
    # Launch lidars
    lidars_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                FindPackageShare("iros_mobile_platform_bringup"),
                "/launch",
                "/lidars.launch.py",
            ]
        )
    )
    # Start battery_node
    battery_node = Node(
        package="iros_mobile_platform_battery",
        executable="battery_monitor",
        name="battery_monitor",
        output="screen",
    )
    iros_mobile_platform_path_planner_launch = IncludeLaunchDescription(
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
            ("use_sim_time", "false"),
            ("slam", LaunchConfiguration("run_mapping")),
            ("map_file", LaunchConfiguration("map_file")),
        ],
    )

    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("iros_mobile_platform_bringup"),
                        "launch",
                        "hardware_control.launch.py",
                    ]
                )
            ]
        )
    )

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
            ("use_sim_time", LaunchConfiguration("use_sim_time")),
        ],
    )

    return LaunchDescription(
        [
            run_mapping,
            map_file,
            use_sim_time,
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
            # Launch the state estimation (odom + ekf)
            encoders_to_odom_node,
            sensor_fusion_launch,
            # Launch the path planner
            iros_mobile_platform_path_planner_launch,
            # Merge two laserscans together
            merge_lidars,
            # Finally launch RViz
            rviz_node,
        ]
    )
