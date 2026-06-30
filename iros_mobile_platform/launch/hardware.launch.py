from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # ── Launch Arguments ──────────────────────────────────────────────────
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

    # ── Hardware Setup: Ports & CAN ───────────────────────────────────────
    # Setup serial port permissions (runs first, fast)
    setup_ports = ExecuteProcess(
        cmd=['bash', '-c',
             'sudo chmod 666 /dev/ttyTHS0 2>/dev/null || true; '
             'sudo chmod 666 /dev/lidar_front 2>/dev/null || true; '
             'sudo chmod 666 /dev/lidar_back 2>/dev/null || true; '
             'echo "[hardware.launch] Ports configured"'],
        name='setup_ports',
        output='screen',
    )

    # Setup CAN bus (slcand for USB-CAN adapter)
    setup_can = ExecuteProcess(
        cmd=['bash', '-c',
             'echo "[hardware.launch] Waiting for CAN adapter..."; '
             'for i in $(seq 1 30); do '
             '  ls /dev/CAN* 2>/dev/null | grep -q CANable && break; '
             '  sleep 0.5; '
             'done; '
             'if ls /dev/CAN* 2>/dev/null | grep -q CANable; then '
             '  sudo slcand -o -c -s6 /dev/CANable can0 && '
             '  sudo ifconfig can0 up && '
             '  sudo ifconfig can0 txqueuelen 2000 && '
             '  echo "[hardware.launch] CAN bus is UP"; '
             'else '
             '  echo "[hardware.launch] WARNING: CAN adapter not found after 15s"; '
             'fi'],
        name='setup_can',
        output='screen',
    )

    # ── RViz ──────────────────────────────────────────────────────────────
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("iros_mobile_platform"), "rviz", "hardware.rviz"]
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    # ── Robot Description (URDF + robot_state_publisher) ──────────────────
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

    # ── Lidars ────────────────────────────────────────────────────────────
    lidars_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                FindPackageShare("iros_mobile_platform_bringup"),
                "/launch",
                "/lidars.launch.py",
            ]
        )
    )

    # ── Lidar Scan Merger ─────────────────────────────────────────────────
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

    # ── CAN Bridge ────────────────────────────────────────────────────────
    socketcan = Node(
        package="ros2socketcan_bridge",
        executable="ros2socketcan",
        name="ros2socketcan",
        output="log",
        arguments=['--ros-args', '--log-level', 'fatal'],
    )

    # ── Motors ────────────────────────────────────────────────────────────
    motor_driver = Node(
        package="iros_mobile_platform_motors",
        executable="motors_driver_node",
        name="motors_driver_node",
        output="screen",
    )

    # ── IMU ───────────────────────────────────────────────────────────────
    imu_node = Node(
        package="jy901s_imu_ros2",
        executable="jy901s_imu_node",
        name="imu_node",
        output="screen",
    )

    # ── Motor Encoders ────────────────────────────────────────────────────
    encoders_node = Node(
        package="iros_mobile_platform_motors",
        executable="encoders_node",
        name="encoders_node",
        output="screen"
    )

    # ── Encoders → Odometry ───────────────────────────────────────────────
    encoders_to_odom_node = Node(
        package="iros_mobile_platform_controller",
        executable="encoders_to_odom",
        name="encoders_to_odom",
        output="screen",
        parameters=[
            {"publish_tf": LaunchConfiguration("publish_tf", default="false")}
        ],
    )

    # ── Sensor Fusion (EKF) ───────────────────────────────────────────────
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

    # ── Controller (diff_drive + rqt_robot_steering) ──────────────────────
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

    # ── Battery Monitor ───────────────────────────────────────────────────
    battery_node = Node(
        package="iros_mobile_platform_battery",
        executable="battery_monitor",
        name="battery_monitor",
        output="screen",
    )

    # ── Path Planner (Nav2) ───────────────────────────────────────────────
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

    # ── Delayed CAN-dependent nodes (wait 3s for CAN bus to come up) ─────
    delayed_can_nodes = TimerAction(
        period=3.0,
        actions=[
            socketcan,
            encoders_node,
            motor_driver,
        ],
    )

    # ── Launch Sequence ───────────────────────────────────────────────────
    return LaunchDescription(
        [
            # 1. Launch arguments
            run_mapping,
            map_file,
            use_sim_time,
            # 2. Hardware setup (ports & CAN)
            setup_ports,
            setup_can,
            # 3. Robot model
            robot_description,
            # 4. Sensors (lidars, IMU)
            lidars_launch,
            imu_node,
            battery_node,
            # 5. CAN-dependent nodes (delayed to let CAN bus initialize)
            delayed_can_nodes,
            # 6. Controller
            controller_launch,
            # 7. State estimation (odometry + EKF)
            encoders_to_odom_node,
            sensor_fusion_launch,
            # 8. Navigation
            iros_mobile_platform_path_planner_launch,
            # 9. Lidar merge
            merge_lidars,
            # 10. RViz
            rviz_node,
        ]
    )
