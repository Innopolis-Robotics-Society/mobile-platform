import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions.declare_launch_argument import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    world_arg = DeclareLaunchArgument(
        "world",
        default_value="simple_office.sdf",
        description="Defines the world that will be used in the simulation. Three worlds are supplied together with the package: \n\n            - 'simple_office.sdf' -> a small office simulation with hardware and actors \n            - 'large_office.sdf' -> a large version of the office with actors, but without furniture \n            - 'clear_world.sdf' -> a scene consisting only of a plane\n\n        To add a new scene, you need to add the world file (.sdf extension) to the 'world' folder. And, if necessary, the models in the 'models' folder.",
    )

    is_custom_controller = DeclareLaunchArgument(
        "enable_custom_controller",
        default_value="True",
        description="Defines the type of robot control:\n\n            - 'True' -> a third-party controller will be used for control \n            - 'False' -> the built-in 'rqt_robot_steernig' controlle  will be used\n",
    )

    custom_controller_pkg = DeclareLaunchArgument(
        "custom_controller_pkg",
        default_value="overlord100_controller",
        description="Defines which ros 2 package will control the robot \n            (works only if the launch argument 'enable_custom_controller' is 'True')",
    )

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )

    spawn_models_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/spawn_models.launch.py",
            ]
        ),
        launch_arguments=[
            ("world", LaunchConfiguration("world")),
            (
                "enable_custom_controller",
                LaunchConfiguration("enable_custom_controller"),
            ),
        ],
    )

    bridge_setup_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/setup_bridges.launch.py",
            ]
        ),
    )

    transforms = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/static_transforms.launch.py",
            ]
        )
    )
    converter = Node(package="overlord100_simulation", executable="converter")

    rviz_node = Node(
        package="rviz2",
        namespace="",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "-d",
            [
                os.path.join(
                    get_package_share_directory("overlord100_simulation"),
                    "rviz",
                    "simulator.rviz",
                )
            ],
        ],
    )

    controller = Node(
        package=LaunchConfiguration("custom_controller_pkg"),
        executable="diff_drive_controller",
        condition=IfCondition(LaunchConfiguration("enable_custom_controller")),
    )

    rqt_node_with_default_controller = Node(
        package="rqt_robot_steering",
        executable="rqt_robot_steering",
        remappings=[
            ("/cmd_vel", "/regular_driver"),
        ],
        condition=UnlessCondition(LaunchConfiguration("enable_custom_controller")),
    )

    rqt_node_with_custom_controller = Node(
        package="rqt_robot_steering",
        executable="rqt_robot_steering",
        condition=IfCondition(LaunchConfiguration("enable_custom_controller")),
    )

    joint_state_broadcaster = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="joint_state_broadcaster",
        output="screen",
        parameters=[
            {
                "use_sim_time": LaunchConfiguration("use_sim_time"),
                "joint_state_broadcast_rate": 50.0,
            }
        ],
    )

    return LaunchDescription(
        [
            world_arg,
            is_custom_controller,
            custom_controller_pkg,
            use_sim_time,
            spawn_models_node,
            bridge_setup_node,
            transforms,
            converter,
            rviz_node,
            controller,
            rqt_node_with_default_controller,
            rqt_node_with_custom_controller,
            joint_state_broadcaster,
        ]
    )
